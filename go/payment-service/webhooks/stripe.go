package webhooks

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/stripe/stripe-go/v76"
	"github.com/stripe/stripe-go/v76/webhook"
)

type WithdrawalStatus string

const (
	StatusPending    WithdrawalStatus = "PENDING"
	StatusProcessing WithdrawalStatus = "PROCESSING"
	StatusArrived    WithdrawalStatus = "ARRIVED"
	StatusFailed     WithdrawalStatus = "FAILED"
)

func StripeHandler(w http.ResponseWriter, r *http.Request) {
	const MaxBodyBytes = int64(65536)
	r.Body = http.MaxBytesReader(w, r.Body, MaxBodyBytes)
	payload, err := io.ReadAll(r.Body)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading request body: %v\n", err)
		w.WriteHeader(http.StatusServiceUnavailable)
		return
	}

	endpointSecret := os.Getenv("STRIPE_WEBHOOK_SECRET")

	event, err := webhook.ConstructEvent(payload, r.Header.Get("Stripe-Signature"), endpointSecret)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error verifying webhook signature: %v\n", err)
		w.WriteHeader(http.StatusBadRequest) // Return a 400 error on a bad signature
		return
	}

	switch event.Type {
	case "payout.paid":
		handlePayoutStatus(event.Data.Object, StatusProcessing)
	case "payout.failed":
		handlePayoutStatus(event.Data.Object, StatusFailed)
	case "transfer.paid":
		handlePayoutStatus(event.Data.Object, StatusArrived)
	default:
		fmt.Fprintf(os.Stdout, "Unhandled event type: %s\n", event.Type)
	}

	w.WriteHeader(http.StatusOK)
}

func handlePayoutStatus(obj json.RawMessage, status WithdrawalStatus) {
	var payout stripe.Payout
	err := json.Unmarshal(obj, &payout)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error unmarshalling stripe object: %v\n", err)
		return
	}

	fmt.Printf("Updating payout %s to status %s\n", payout.ID, status)

	// 1. Update PostgreSQL (simulation)
	updateDB(payout.ID, status)

	// 2. Push to WebSocket via Rust API (simulation)
	broadcastToDashboard(payout.ID, status, payout.Amount)

	// 3. Send Telegram (simulation)
	sendTelegram(status, payout.Amount)
}

func updateDB(id string, status WithdrawalStatus) {
	fmt.Printf("DB: Withdrawal %s set to %s\n", id, status)
}

func broadcastToDashboard(id string, status WithdrawalStatus, amount int64) {
	fmt.Printf("WS: Broadcasting update for %s\n", id)
	url := os.Getenv("RUST_API_URL")
	if url == "" {
		url = "http://localhost:8000"
	}

	payload := map[string]interface{}{
		"event_type": "WITHDRAWAL_UPDATE",
		"payload": map[string]interface{}{
			"payout_id": id,
			"status":    status,
			"amount":    float64(amount) / 100.0,
		},
	}

	data, _ := json.Marshal(payload)
	resp, err := http.Post(url+"/internal/broadcast", "application/json", bytes.NewBuffer(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error broadcasting to dashboard: %v\n", err)
		return
	}
	defer resp.Body.Close()
}

func sendTelegram(status WithdrawalStatus, amount int64) {
	msg := ""
	amt := float64(amount) / 100.0
	switch status {
	case StatusArrived:
		msg = fmt.Sprintf("✅ Money arrived — $%.2f — %s", amt, "now")
	case StatusFailed:
		msg = fmt.Sprintf("❌ Transfer failed — $%.2f — funds returned to balance", amt)
	}
	if msg != "" {
		fmt.Printf("Telegram: %s\n", msg)
	}
}

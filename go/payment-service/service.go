package payment

import (
	"context"
	"fmt"
	"time"

	"github.com/stripe/stripe-go/v76"
	"github.com/stripe/stripe-go/v76/customer"
	"github.com/stripe/stripe-go/v76/paymentintent"
)

type PaymentService struct {
	StripeSecret string
	Bills        []Bill
}

func NewPaymentService(secret string) *PaymentService {
	stripe.Key = secret
	return &PaymentService{
		StripeSecret: secret,
	}
}

func (s *PaymentService) Charge(customerEmail string, amount int64) (string, error) {
	// 1. Create or get customer
	params := &stripe.CustomerParams{
		Email: stripe.String(customerEmail),
	}
	cust, err := customer.New(params)
	if err != nil {
		return "", err
	}

	// 2. Create PaymentIntent
	piParams := &stripe.PaymentIntentParams{
		Amount:   stripe.Int64(amount),
		Currency: stripe.String(string(stripe.CurrencyUSD)),
		Customer: stripe.String(cust.ID),
	}
	pi, err := paymentintent.New(piParams)
	if err != nil {
		return "", err
	}

	fmt.Printf("Stripe: PaymentIntent created %s for %s\n", pi.ID, customerEmail)
	return pi.ID, nil
}

func (s *PaymentService) PurchaseAPI(apiName string, cost float64) (string, error) {
	// Logic to subscribe to an external API
	fmt.Printf("Payment: Automating API subscription for %s - $%.2f/mo\n", apiName, cost)
	s.Bills = append(s.Bills, Bill{
		ID:        fmt.Sprintf("api_%d", time.Now().Unix()),
		Provider:  apiName,
		Amount:    cost,
		Category:  "API_SUBSCRIPTION",
		Timestamp: time.Now(),
	})
	// In reality, this would return a key after successful signup automation
	return "sk_live_v2_key_" + apiName, nil
}

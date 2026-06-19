package billing

import (
	"time"
)

type Category string

const (
	API    Category = "API"
	INFRA  Category = "INFRA"
	HIRING Category = "HIRING"
	SOCIAL Category = "SOCIAL"
)

type Bill struct {
	ID        string    `json:"id"`
	Category  Category  `json:"category"`
	Provider  string    `json:"provider"`
	Amount    float64   `json:"amount"`
	Timestamp time.Time `json:"timestamp"`
}

type Tracker struct {
	History []Bill
}

func NewTracker() *Tracker {
	return &Tracker{History: make([]Bill, 0)}
}

func (t *Tracker) Record(cat Category, provider string, amount float64) {
	t.History = append(t.History, Bill{
		ID:        time.Now().Format("20060102150405"),
		Category:  cat,
		Provider:  provider,
		Amount:    amount,
		Timestamp: time.Now(),
	})
}

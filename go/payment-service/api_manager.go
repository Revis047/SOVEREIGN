package payment

import (
	"fmt"
	"github.com/ver/sovereign-omega/payment-service/billing"
)

type APICreds struct {
	Name   string
	Key    string
	Active bool
}

type APIManager struct {
	Registry map[string]APICreds
	Tracker  *billing.Tracker
}

func NewAPIManager(tracker *billing.Tracker) *APIManager {
	return &APIManager{
		Registry: make(map[string]APICreds),
		Tracker:  tracker,
	}
}

func (m *APIManager) AcquireAPI(name string, cost float64) error {
	fmt.Printf("API: Autonomous Acquisition of %s initiated\n", name)
	// In production, this would use Stripe to pay and then store the key in Vault
	m.Registry[name] = APICreds{Name: name, Key: "sk_autonomous_" + name, Active: true}
	m.Tracker.Record(billing.API, name, cost)
	return nil
}

func (m *APIManager) Connect(name string) (string, error) {
	if creds, ok := m.Registry[name]; ok && creds.Active {
		return creds.Key, nil
	}
	return "", fmt.Errorf("API %s not acquired or inactive", name)
}

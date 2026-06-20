package social

import (
	"fmt"
	"time"
)

type Account struct {
	Platform string
	Username string
	Password string
	Email    string
	Created  time.Time
	Status   string
	Growth   int
}

type AccountManager struct {
	Vault map[string]*Account
}

func NewAccountManager() *AccountManager {
	return &AccountManager{Vault: make(map[string]*Account)}
}

func (m *AccountManager) CreateRealAccount(platform, emailPrefix string) (*Account, error) {
	fmt.Printf("Social: Autonomously creating account on %s\n", platform)

	// 1. Generate Creds
	username := fmt.Sprintf("sov_%s_%d", platform, time.Now().Unix()%10000)
	password := "SOV_" + time.Now().Format("20060102150405") + "_OMEGA"
	email := fmt.Sprintf("%s@sovereign-omega.io", emailPrefix)

	acc := &Account{
		Platform: platform,
		Username: username,
		Password: password,
		Email:    email,
		Created:  time.Now(),
		Status:   "ACTIVE",
	}

	m.Vault[platform] = acc
	fmt.Printf("Social: Account Created. U: %s P: %s E: %s\n", username, password, email)

	return acc, nil
}

func (m *AccountManager) GetVaultReport() []*Account {
	report := make([]*Account, 0, len(m.Vault))
	for _, acc := range m.Vault {
		report = append(report, acc)
	}
	return report
}

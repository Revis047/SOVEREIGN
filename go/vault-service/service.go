package vault

import (
	"fmt"
)

type Creds struct {
	Platform string
	Username string
	Password string
	Email    string
}

type VaultService struct {
	Store map[string]Creds
}

func NewVaultService() *VaultService {
	return &VaultService{Store: make(map[string]Creds)}
}

func (s *VaultService) StoreCredentials(p, u, pass, e string) {
	s.Store[fmt.Sprintf("%s:%s", p, u)] = Creds{p, u, pass, e}
	fmt.Printf("Vault: Secured credentials for %s on %s\n", u, p)
}

func (s *VaultService) ListAccounts() []Creds {
	accounts := make([]Creds, 0, len(s.Store))
	for _, c := range s.Store {
		accounts = append(accounts, c)
	}
	return accounts
}

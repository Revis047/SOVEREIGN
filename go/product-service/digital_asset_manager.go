package product

import (
	"fmt"
	"strings"
)

type TokenConfig struct {
	Symbol      string
	TotalSupply int64
	Utility     string
	PlatformID  string
}

type InternalEconomyRules struct {
	EarnRate     float64 // tokens per participation unit
	BurnRate     float64 // tokens burned per transaction
	UnlockRules  map[string]int64
}

type DigitalAssetManager struct {
	ActiveTokens []TokenConfig
}

func (m *DigitalAssetManager) IssueUtilityToken(config TokenConfig) error {
	fmt.Printf("DigitalAsset: Initiating token issuance for %s (Utility: %s)\n", config.Symbol, config.Utility)

	// Compliance Check (Utility Token Framework)
	if !m.verifyUtilityStructure(config) {
		return fmt.Errorf("token structure does not meet utility compliance requirements: potential security classification")
	}

	fmt.Printf("DigitalAsset: Token %s issued successfully. Total supply: %d units. Distributed to ecosystem treasury.\n", config.Symbol, config.TotalSupply)
	m.ActiveTokens = append(m.ActiveTokens, config)
	return nil
}

func (m *DigitalAssetManager) verifyUtilityStructure(config TokenConfig) bool {
	// Rule: Token must provide access, discount, or rights within a specific system
	// and not promise dividends or passive profit from effort of others.
	if config.Utility == "" {
		return false
	}
	return !m.containsInvestmentKeywords(config.Utility)
}

func (m *DigitalAssetManager) containsInvestmentKeywords(utility string) bool {
	keywords := []string{"profit", "dividend", "investment", "passive income", "roi", "yield", "guaranteed"}
	lowerUtility := strings.ToLower(utility)
	for _, kw := range keywords {
		if strings.Contains(lowerUtility, kw) {
			return true
		}
	}
	return false
}

func (m *DigitalAssetManager) DesignCommunityCurrency(platformName string) *InternalEconomyRules {
	fmt.Printf("DigitalAsset: Designing internal economy for %s\n", platformName)
	rules := &InternalEconomyRules{
		EarnRate: 10.0,
		BurnRate: 0.05,
		UnlockRules: map[string]int64{
			"premium_access": 500,
			"early_listing": 200,
			"custom_domain": 1000,
		},
	}
	fmt.Printf("DigitalAsset: Economy rules for %s finalized. Earn: %.2f, Burn: %.2f\n", platformName, rules.EarnRate, rules.BurnRate)
	return rules
}

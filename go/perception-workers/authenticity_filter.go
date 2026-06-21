package perception

import (
	"fmt"
	"strings"
	"time"
)

type SignalType string

const (
	SignalReview   SignalType = "REVIEW"
	SignalSocial   SignalType = "SOCIAL"
	SignalTrend    SignalType = "TREND"
	SignalEvidence SignalType = "EVIDENCE"
)

type Signal struct {
	Type      SignalType
	Content   string
	Source    string
	Metadata  map[string]string
	Timestamp time.Time
}

type AuthenticityReport struct {
	Authentic bool
	Score     float64
	Reason    string
}

type SignalAuthenticityLayer struct{}

func NewSignalAuthenticityLayer() *SignalAuthenticityLayer {
	return &SignalAuthenticityLayer{}
}

func (l *SignalAuthenticityLayer) Filter(signal Signal) AuthenticityReport {
	switch signal.Type {
	case SignalReview:
		return l.checkReviewAuthenticity(signal)
	case SignalSocial:
		return l.checkSocialAuthenticity(signal)
	case SignalTrend:
		return l.checkTrendAuthenticity(signal)
	case SignalEvidence:
		return l.checkEvidenceAuthenticity(signal)
	default:
		return AuthenticityReport{Authentic: true, Score: 1.0}
	}
}

func (l *SignalAuthenticityLayer) checkReviewAuthenticity(s Signal) AuthenticityReport {
	// Pattern: Burst language, uniform clusters, lack of detail
	text := strings.ToLower(s.Content)
	if strings.Contains(text, "best ever") && len(text) < 30 {
		return AuthenticityReport{Authentic: false, Score: 0.1, Reason: "Uniform language cluster / Low detail"}
	}

	// Check for "burst" pattern in metadata (simulated)
	if s.Metadata["frequency_24h"] == "HIGH_ANOMALY" {
		return AuthenticityReport{Authentic: false, Score: 0.05, Reason: "Temporal burst pattern detected"}
	}

	return AuthenticityReport{Authentic: true, Score: 0.9}
}

func (l *SignalAuthenticityLayer) checkSocialAuthenticity(s Signal) AuthenticityReport {
	// Pattern: Engagement anomaly vs follower count
	followers := s.Metadata["followers"]
	engagement := s.Metadata["engagement_rate"]

	if engagement == "HIGH" && followers == "LOW" {
		return AuthenticityReport{Authentic: false, Score: 0.2, Reason: "Hollow account depth / Engagement anomaly"}
	}

	return AuthenticityReport{Authentic: true, Score: 0.85}
}

func (l *SignalAuthenticityLayer) checkTrendAuthenticity(s Signal) AuthenticityReport {
	// Pattern: Coverage spike with no organic search correlation
	if s.Metadata["organic_search_volume"] == "LOW" && s.Metadata["media_mentions"] == "HIGH" {
		return AuthenticityReport{Authentic: false, Score: 0.15, Reason: "Manufactured trend / No organic correlation"}
	}
	return AuthenticityReport{Authentic: true, Score: 0.95}
}

func (l *SignalAuthenticityLayer) checkEvidenceAuthenticity(s Signal) AuthenticityReport {
	// Pattern: Claim-to-evidence ratio anomaly
	if strings.Contains(s.Content, "M") && !strings.Contains(s.Metadata["verifiable_signals"], "STRIPE_API") {
		return AuthenticityReport{Authentic: false, Score: 0.0, Reason: "Fabricated proof / No corroborating signals"}
	}
	return AuthenticityReport{Authentic: true, Score: 1.0}
}

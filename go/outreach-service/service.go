package outreach

import (
	"fmt"
)

type OutreachService struct {
	DailyLimit int
	SentToday  int
}

func (s *OutreachService) SendColdEmail(targetEmail, body string) error {
	if s.SentToday >= s.DailyLimit {
		return fmt.Errorf("OUTREACH_LIMIT_EXCEEDED: %d/day", s.DailyLimit)
	}
	fmt.Printf("Outreach: Sending autonomous email to %s\n", targetEmail)
	s.SentToday++
	return nil
}

func (s *OutreachService) LinkedInConnect(profileURL, message string) error {
	fmt.Printf("Outreach: Sending LinkedIn request to %s\n", profileURL)
	return nil
}

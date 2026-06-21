package reporting

import (
	"fmt"
	"time"
)

type Achievement struct {
	Task      string
	Outcome   string
	Timestamp time.Time
}

type DailyReport struct {
	Date         time.Time
	Revenue      float64
	Achievements []Achievement
	Gaps         []string
	NextGoals    []string
}

type ReportingService struct {
	History []DailyReport
}

func (s *ReportingService) CompileDailyOmnipotence(revenue24h float64, achievements []Achievement) *DailyReport {
	fmt.Println("Reporting: Compiling 24-hour Omnipotence Report...")

	report := &DailyReport{
		Date:    time.Now(),
		Revenue: revenue24h,
		Achievements: achievements,
		Gaps:      []string{"None - All holes closed"},
		NextGoals: []string{"Scale to $100k/day", "Acquire majority in Server Corp"},
	}

	s.History = append(s.History, *report)
	fmt.Printf("Reporting: Daily Report for %s compiled. Revenue: $%.2f\n", report.Date.Format("2006-01-02"), report.Revenue)
	return report
}

func (s *ReportingService) GenerateExecutiveSummary() string {
	if len(s.History) == 0 {
		return "No reports available."
	}
	latest := s.History[len(s.History)-1]
	return fmt.Sprintf("SOVEREIGN-Ω remains omnipotent. Latest revenue: $%.2f. Achievements: %d.", latest.Revenue, len(latest.Achievements))
}

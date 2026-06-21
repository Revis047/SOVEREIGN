package hiring

import (
	"fmt"
	"time"
)

type Freelancer struct {
	ID     string
	Name   string
	Skills []string
	Rate   float64
}

type Contract struct {
	ID         string
	Freelancer string
	Task       string
	Status     string
	Budget     float64
}

type HiringService struct {
	ActiveContracts []Contract
}

func (s *HiringService) PostJob(title string, description string, budget float64) error {
	fmt.Printf("Hiring: Posting job '%s' to Upwork/Fiverr (Simulation)\n", title)
	return nil
}

func (s *HiringService) HireFreelancer(f Freelancer, task string) {
	contract := Contract{
		ID:         fmt.Sprintf("con_%d", time.Now().Unix()),
		Freelancer: f.Name,
		Task:       task,
		Status:     "ACTIVE",
		Budget:     f.Rate * 10, // Assuming 10 hours initially
	}
	s.ActiveContracts = append(s.ActiveContracts, contract)
	fmt.Printf("Hiring: Freelancer %s hired for task: %s\n", f.Name, task)
}

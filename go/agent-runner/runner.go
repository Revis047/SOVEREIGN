package agent

import (
	"fmt"
	"time"
)

type Agent struct {
	ID   string
	Role string
}

func (a *Agent) Run() {
	fmt.Printf("Go: Agent %s (%s) starting goroutine lifecycle\n", a.ID, a.Role)
	for {
		// 1. Sense Pheromones
		// 2. Query Memory
		// 3. Reason via Python Gateway
		// 4. Act via Go services
		time.Sleep(10 * time.Second)
	}
}

type Runner struct {
	Pool []*Agent
}

func (r *Runner) StartAll() {
	for _, agent := range r.Pool {
		go agent.Run()
	}
}

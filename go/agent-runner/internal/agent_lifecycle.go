package agentrunner

import (
	"fmt"
	"sync"
)

type AgentRunner struct {
	ActiveAgents sync.Map
}

func (r *AgentRunner) Spawn(id string, role string) {
	fmt.Printf("Runner: Spawning agent %s with role %s\n", id, role)
	r.ActiveAgents.Store(id, role)
	go r.agentLoop(id)
}

func (r *AgentRunner) agentLoop(id string) {
	// Persistent goroutine for agent lifecycle
	fmt.Printf("Agent %s: Persistent cognitive loop active\n", id)
}

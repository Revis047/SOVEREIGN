package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/ver/sovereign-omega/payment-service"
	"github.com/ver/sovereign-omega/perception-workers"
	"github.com/ver/sovereign-omega/reporting-service"
	"github.com/ver/sovereign-omega/hiring-service"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8001"
	}

	fmt.Printf("SOVEREIGN-Ω :: Go Service Grid :: Starting on port %s\n", port)

	// In a real grid, this would route to sub-services or be a monolith
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "OK")
	})

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		panic(err)
	}
}

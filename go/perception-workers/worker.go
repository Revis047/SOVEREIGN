package perception

import (
	"context"
	"fmt"
	"net/http"
	"strings"
	"sync"

	"github.com/PuerkitoBio/goquery"
)

type MarketOpportunity struct {
	Niche      string
	Velocity   float64
	UnmetNeeds []string
	Source     string
}

type MorphicWorker struct {
	ID string
}

func (w *MorphicWorker) ScanNiche(ctx context.Context, url string) ([]string, error) {
	fmt.Printf("Perception Worker %s: Scraping %s for pain points...\n", w.ID, url)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("status code error: %d %s", resp.StatusCode, resp.Status)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, err
	}

	var findings []string
	doc.Find("p, span, h1, h2, h3, li").Each(func(i int, s *goquery.Selection) {
		text := s.Text()
		textLower := strings.ToLower(text)
		if strings.Contains(textLower, "problem with") ||
		   strings.Contains(textLower, "wish i had") ||
		   strings.Contains(textLower, "frustrated by") ||
		   strings.Contains(textLower, "annoying") {
			findings = append(findings, strings.TrimSpace(text))
		}
	})

	return findings, nil
}

type IngestionPipeline struct {
	Workers []MorphicWorker
	Targets []string
}

func (p *IngestionPipeline) Start(ctx context.Context) {
	fmt.Printf("Perception: Starting high-throughput ingestion pipeline for %d targets\n", len(p.Targets))

	var wg sync.WaitGroup
	for _, url := range p.Targets {
		wg.Add(1)
		go func(target string) {
			defer wg.Done()
			worker := p.Workers[0] // Simple worker allocation for demo
			findings, err := worker.ScanNiche(ctx, target)
			if err == nil && len(findings) > 0 {
				fmt.Printf("Perception: Discovered %d pain points on %s\n", len(findings), target)
				// Here we would push findings to Sovereign Bus
			}
		}(url)
	}
	wg.Wait()
}

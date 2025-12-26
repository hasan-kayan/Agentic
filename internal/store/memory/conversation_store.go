package memory

import (
	"context"
	"sync"
	"time"

	"github.com/hasan-kayan/Agentic/internal/domain/chat"
)

type Store struct {
	mu sync.RWMutex
	m  map[string][]chat.Message
}

func New() *Store {
	return &Store{
		m: make(map[string][]chat.Message),
	}
}

func (s *Store) Get(_ context.Context, conversationID string) ([]chat.Message, bool, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	msgs, ok := s.m[conversationID]
	if !ok {
		return nil, false, nil
	}

	// defensive copy
	out := make([]chat.Message, len(msgs))
	copy(out, msgs)
	return out, true, nil
}

func (s *Store) Put(_ context.Context, conversationID string, messages []chat.Message) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	out := make([]chat.Message, len(messages))
	copy(out, messages)

	// normalize timestamps (optional)
	now := time.Now()
	for i := range out {
		if out[i].CreatedAt.IsZero() {
			out[i].CreatedAt = now
		}
	}

	s.m[conversationID] = out
	return nil
}

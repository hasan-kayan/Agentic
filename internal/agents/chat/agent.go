package chat

import (
	"context"
	"time"

	"github.com/google/uuid"

	dchat "github.com/hasan-kayan/Agentic/internal/domain/chat"
	"github.com/hasan-kayan/Agentic/internal/llm"
	"github.com/hasan-kayan/Agentic/internal/store"
)

type Agent struct {
	llm        llm.Client
	store      store.ConversationStore
	system     string
	model      string
	maxHistory int
}

func New(llmClient llm.Client, st store.ConversationStore, systemPrompt, model string, maxHistory int) *Agent {
	return &Agent{
		llm:        llmClient,
		store:      st,
		system:     systemPrompt,
		model:      model,
		maxHistory: maxHistory,
	}
}

func (a *Agent) Reply(ctx context.Context, conversationID string, userMessage string) (dchat.ChatResponse, error) {
	if conversationID == "" {
		conversationID = uuid.NewString()
	}

	history, ok, err := a.store.Get(ctx, conversationID)
	if err != nil {
		return dchat.ChatResponse{}, err
	}
	if !ok {
		history = []dchat.Message{}
	}

	// build messages
	msgs := make([]dchat.Message, 0, 2+len(history))
	if a.system != "" {
		msgs = append(msgs, dchat.Message{Role: dchat.RoleSystem, Content: a.system, CreatedAt: time.Now()})
	}

	// append trimmed history
	h := trimTail(history, a.maxHistory)
	msgs = append(msgs, h...)

	// append new user message
	userMsg := dchat.Message{Role: dchat.RoleUser, Content: userMessage, CreatedAt: time.Now()}
	msgs = append(msgs, userMsg)

	reply, err := a.llm.ChatOnce(ctx, a.model, msgs)
	if err != nil {
		return dchat.ChatResponse{}, err
	}

	assistantMsg := dchat.Message{Role: dchat.RoleAssistant, Content: reply, CreatedAt: time.Now()}

	// persist (history WITHOUT system)
	newHistory := append(h, userMsg, assistantMsg)
	if err := a.store.Put(ctx, conversationID, newHistory); err != nil {
		return dchat.ChatResponse{}, err
	}

	return dchat.ChatResponse{
		ConversationID: conversationID,
		Reply:          reply,
		Model:          a.model,
	}, nil
}

func (a *Agent) ReplyStream(ctx context.Context, conversationID string, userMessage string) (string, <-chan llm.StreamEvent, error) {
	if conversationID == "" {
		conversationID = uuid.NewString()
	}

	history, ok, err := a.store.Get(ctx, conversationID)
	if err != nil {
		return "", nil, err
	}
	if !ok {
		history = []dchat.Message{}
	}

	msgs := make([]dchat.Message, 0, 2+len(history))
	if a.system != "" {
		msgs = append(msgs, dchat.Message{Role: dchat.RoleSystem, Content: a.system, CreatedAt: time.Now()})
	}

	h := trimTail(history, a.maxHistory)
	msgs = append(msgs, h...)

	userMsg := dchat.Message{Role: dchat.RoleUser, Content: userMessage, CreatedAt: time.Now()}
	msgs = append(msgs, userMsg)

	stream, err := a.llm.ChatStream(ctx, a.model, msgs)
	if err != nil {
		return "", nil, err
	}

	// Caller will accumulate deltas; when done, persist.
	// (Persisting here would require buffering; API handler does it.)
	return conversationID, stream, nil
}

func trimTail(history []dchat.Message, max int) []dchat.Message {
	if max <= 0 {
		return []dchat.Message{}
	}
	if len(history) <= max {
		out := make([]dchat.Message, len(history))
		copy(out, history)
		return out
	}
	out := make([]dchat.Message, max)
	copy(out, history[len(history)-max:])
	return out
}

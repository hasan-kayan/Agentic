package handlers

import (
	"context"
	"encoding/json"
	"net/http"
	"strings"
	"time"

	"github.com/hasan-kayan/Agentic/internal/agents/chat"
	dchat "github.com/hasan-kayan/Agentic/internal/domain/chat"
	"github.com/hasan-kayan/Agentic/internal/llm"
	"github.com/hasan-kayan/Agentic/internal/store"
)

type ChatHandler struct {
	agent *chat.Agent
	st    store.ConversationStore
}

func NewChatHandler(agent *chat.Agent, st store.ConversationStore) *ChatHandler {
	return &ChatHandler{agent: agent, st: st}
}

func (h *ChatHandler) ChatOnce(w http.ResponseWriter, r *http.Request) {
	var req dchat.ChatRequest
	if err := decodeJSON(r, &req, 1<<20); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	req.Message = strings.TrimSpace(req.Message)
	if req.Message == "" {
		http.Error(w, "message is required", http.StatusBadRequest)
		return
	}

	ctx := r.Context()
	resp, err := h.agent.Reply(ctx, req.ConversationID, req.Message)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	writeJSON(w, http.StatusOK, resp)
}

func (h *ChatHandler) ChatStream(w http.ResponseWriter, r *http.Request) {
	var req dchat.ChatRequest
	if err := decodeJSON(r, &req, 1<<20); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	req.Message = strings.TrimSpace(req.Message)
	if req.Message == "" {
		http.Error(w, "message is required", http.StatusBadRequest)
		return
	}

	ctx := r.Context()

	convID, stream, err := h.agent.ReplyStream(ctx, req.ConversationID, req.Message)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	// SSE headers
	w.Header().Set("Content-Type", "text/event-stream; charset=utf-8")
	w.Header().Set("Cache-Control", "no-cache, no-transform")
	w.Header().Set("Connection", "keep-alive")

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "streaming not supported", http.StatusInternalServerError)
		return
	}

	// send conversation_id as first event
	sse(w, "meta", map[string]any{"conversation_id": convID})
	flusher.Flush()

	// accumulate for persistence
	var buf strings.Builder
	for ev := range stream {
		if ev.Err != nil {
			sse(w, "error", map[string]any{"message": ev.Err.Error()})
			flusher.Flush()
			return
		}
		if ev.Delta != "" {
			buf.WriteString(ev.Delta)
			sse(w, "delta", map[string]any{"delta": ev.Delta})
			flusher.Flush()
		}
		if ev.Done {
			break
		}
	}

	// persist final assistant message (history WITHOUT system)
	if err := persistStreamResult(ctx, h.st, convID, req.Message, buf.String()); err != nil {
		// don’t kill stream; just notify
		sse(w, "warn", map[string]any{"message": "persist_failed", "detail": err.Error()})
		flusher.Flush()
	}

	sse(w, "done", map[string]any{"ok": true})
	flusher.Flush()
}

func persistStreamResult(ctx context.Context, st store.ConversationStore, convID, userText, assistantText string) error {
	history, ok, err := st.Get(ctx, convID)
	if err != nil {
		return err
	}
	if !ok {
		history = []dchat.Message{}
	}

	now := time.Now()
	userMsg := dchat.Message{Role: dchat.RoleUser, Content: userText, CreatedAt: now}
	asstMsg := dchat.Message{Role: dchat.RoleAssistant, Content: assistantText, CreatedAt: time.Now()}

	history = append(history, userMsg, asstMsg)
	return st.Put(ctx, convID, history)
}

func decodeJSON(r *http.Request, v any, maxBytes int64) error {
	r.Body = http.MaxBytesReader(nil, r.Body, maxBytes)
	dec := json.NewDecoder(r.Body)
	dec.DisallowUnknownFields()
	return dec.Decode(v)
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func sse(w http.ResponseWriter, event string, payload any) {
	b, _ := json.Marshal(payload)
	_, _ = w.Write([]byte("event: " + event + "\n"))
	_, _ = w.Write([]byte("data: " + string(b) + "\n\n"))
}

// Ensure interface usage (compile-time)
var _ = llm.StreamEvent{}

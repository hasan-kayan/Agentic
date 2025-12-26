package openai

import (
	"context"
	"errors"

	openai "github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
	"github.com/openai/openai-go/v3/shared"

	"github.com/hasan-kayan/Agentic/internal/domain/chat"
	"github.com/hasan-kayan/Agentic/internal/llm"
)

type Client struct {
	c *openai.Client
}

func New(apiKey string) *Client {
	return &Client{
		c: openai.NewClient(option.WithAPIKey(apiKey)),
	}
}

func (x *Client) ChatOnce(ctx context.Context, model string, messages []chat.Message) (string, error) {
	params := openai.ChatCompletionNewParams{
		Model:    shared.ChatModel(model),
		Messages: toSDKMessages(messages),
	}

	resp, err := x.c.Chat.Completions.New(ctx, params)
	if err != nil {
		return "", err
	}
	if len(resp.Choices) == 0 {
		return "", errors.New("empty choices")
	}
	return resp.Choices[0].Message.Content, nil
}

func (x *Client) ChatStream(ctx context.Context, model string, messages []chat.Message) (<-chan llm.StreamEvent, error) {
	params := openai.ChatCompletionNewParams{
		Model:    shared.ChatModel(model),
		Messages: toSDKMessages(messages),
	}

	stream := x.c.Chat.Completions.NewStreaming(ctx, params)

	ch := make(chan llm.StreamEvent, 64)
	go func() {
		defer close(ch)
		defer stream.Close()

		for stream.Next() {
			chunk := stream.Current()
			if len(chunk.Choices) > 0 {
				delta := chunk.Choices[0].Delta.Content
				if delta != "" {
					ch <- llm.StreamEvent{Delta: delta}
				}
			}
		}
		if err := stream.Err(); err != nil {
			ch <- llm.StreamEvent{Err: err}
			return
		}
		ch <- llm.StreamEvent{Done: true}
	}()

	return ch, nil
}

func toSDKMessages(msgs []chat.Message) []openai.ChatCompletionMessageParamUnion {
	out := make([]openai.ChatCompletionMessageParamUnion, 0, len(msgs))
	for _, m := range msgs {
		switch m.Role {
		case chat.RoleSystem:
			out = append(out, openai.SystemMessage(m.Content))
		case chat.RoleAssistant:
			out = append(out, openai.AssistantMessage(m.Content))
		default:
			out = append(out, openai.UserMessage(m.Content))
		}
	}
	return out
}

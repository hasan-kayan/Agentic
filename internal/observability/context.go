package observability

import (
	"context"

	"go.uber.org/zap"
)

type ctxKey int

const loggerKey ctxKey = 1

func WithLogger(ctx context.Context, l *zap.Logger) context.Context {
	return context.WithValue(ctx, loggerKey, l)
}

func FromContext(ctx context.Context) *zap.Logger {
	if v := ctx.Value(loggerKey); v != nil {
		if l, ok := v.(*zap.Logger); ok {
			return l
		}
	}
	return zap.NewNop()
}

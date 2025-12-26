package observability

import "go.uber.org/zap"

func RequestID(v string) zap.Field { return zap.String("request_id", v) }
func TraceID(v string) zap.Field   { return zap.String("trace_id", v) }
func AgentID(v string) zap.Field   { return zap.String("agent_id", v) }
func RunID(v string) zap.Field     { return zap.String("run_id", v) }
func Component(v string) zap.Field { return zap.String("component", v) }

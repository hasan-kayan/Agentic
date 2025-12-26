package observability

import (
	"os"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

type LoggerConfig struct {
	Service string
	Env     string
	Version string
	GitSHA  string
	Level   string // debug/info/warn/error
}

func NewLogger(cfg LoggerConfig) (*zap.Logger, func(), error) {
	level := zapcore.InfoLevel
	_ = level.Set(cfg.Level)

	encCfg := zap.NewProductionEncoderConfig()
	encCfg.TimeKey = "ts"
	encCfg.LevelKey = "level"
	encCfg.MessageKey = "msg"
	encCfg.EncodeTime = zapcore.ISO8601TimeEncoder

	core := zapcore.NewCore(
		zapcore.NewJSONEncoder(encCfg),
		zapcore.AddSync(os.Stdout),
		level,
	)

	l := zap.New(core, zap.AddCaller(), zap.AddStacktrace(zapcore.ErrorLevel)).
		With(
			zap.String("service", cfg.Service),
			zap.String("env", cfg.Env),
			zap.String("version", cfg.Version),
			zap.String("git_sha", cfg.GitSHA),
		)

	cleanup := func() { _ = l.Sync() }
	return l, cleanup, nil
}

# 11 - Performance Tuning

## Producer tuning
- Increase `batch.size` and `linger.ms` for throughput.
- Use `compression.type` (lz4 or zstd) to reduce bandwidth.
- Use `acks=all` and idempotence for safe retries.

## Consumer tuning
- Increase `fetch.min.bytes` and `fetch.max.bytes`.
- Increase `max.poll.records` for batch processing.
- Ensure processing time is below `max.poll.interval.ms`.

## Broker tuning
- `num.network.threads` and `num.io.threads` sized for workload.
- Use SSDs and ensure enough page cache.
- Set `log.segment.bytes` to manage segment roll frequency.

## Partition sizing
- Target partitions per broker within operational limits.
- Use enough partitions to match consumer parallelism.
- Avoid partition counts that exceed disk throughput.

## Common bottlenecks
- Single hot partition due to skewed keys
- Small batch sizes with high overhead
- Slow disks causing log flush delays

Next: `12-troubleshooting/README.md`

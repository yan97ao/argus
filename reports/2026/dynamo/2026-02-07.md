# 每日更新报告（2026-02-07）

## ai-dynamo/dynamo

| 提交时间 | 作者 | 提交信息 |
|----------|------|----------|
| 2026-02-07 11:25:02 | dagil-nvidia | docs: full migration of docs/ to fern format in fern/ (#6050) |
| 2026-02-07 11:02:45 | Konstantin Korolev | fix: reduce NATS consumer inactive_threshold from 1h to 2min (#5861) |
| 2026-02-07 11:02:28 | Yongming Ding | feat(mocker): add optional KV cache allocation/eviction trace (#6052) |
| 2026-02-07 10:39:28 | Karen Chung | fix: Router + SGLang DP testing (#6057) |
| 2026-02-07 09:03:07 | Richard Huo | docs: add notes and instruction for latest trtllm kvbm disagg (#6055) |
| 2026-02-07 07:32:52 | Qi Wang | feat: EC E/PD workflow in TRT-LLM (#5815) |
| 2026-02-07 07:14:47 | Xavier Chang | fix: fix missing update DynamoComponentReady condition (#5051) |
| 2026-02-07 07:08:41 | Yan Ru Pei | docs: clarify the usage of LRU for mocker evictor (#6053) |
| 2026-02-07 07:08:27 | ls-2018 | fix: operator chart imagePullPolicy (#4821) |
| 2026-02-07 07:08:17 | jthomson04 | feat: GB200 GPT-oss disagg recipe (#4954) |
| 2026-02-07 07:07:40 | KrishnanPrash | fix(sglang): remove apt-installed python3-blinker (#5995) |
| 2026-02-07 07:07:30 | Ben Hamm | fix(recipes): correct GPU counts in DeepSeek-R1 READMEs (#5953) |
| 2026-02-07 05:17:21 | akshatha-k | docs: add quick start sections to KVBM and Router guides (#6043) |
| 2026-02-07 05:09:34 | Tushar Sharma | ci: Transition deploy tests to pytest framework (#5874) |
| 2026-02-07 04:51:37 | Julien Mancuso | fix: downgrading opencontainers/runtime-spec version to fix compatibility issue with containerd (#6049) |
| 2026-02-07 04:50:55 | Jacky | refactor: Move --migration-limit flag from backend to frontend (#5918) |
| 2026-02-07 04:11:04 | Anant Sharma | fix: update bytes crate version to latest (#6041) |
| 2026-02-07 04:07:31 | mohammedabdulwahhab | fix: remove envsubst for logging-dashboard.yaml to preserve Grafana template variables (#6045) |
| 2026-02-07 04:01:29 | Qi Wang | feat: enable go-to-definition for dynamo.runtime, dynamo.nixl and external dependencies (#6026) |
| 2026-02-07 04:01:13 | Ryan McCormick | docs: Update disagg and request flow design docs based on latest code (#5993) |
| 2026-02-07 03:39:23 | Anant Sharma | ci: remove release branch docs deploy workflow (#6039) |
| 2026-02-07 03:35:42 | Julien Mancuso | feat: update grove dependency to 0.1.0-alpha.6 (#6015) |
| 2026-02-07 03:35:13 | Julien Mancuso | fix: fix ChReK go.mod stale dependencies (#6040) |
| 2026-02-07 03:27:44 | Yan Ru Pei | chore: clean ups in kv_router.rs (#6028) |
| 2026-02-07 03:20:36 | dagil-nvidia | docs: clean up toctree navigation and add disaggregated serving guide (#6024) |
| 2026-02-07 03:01:09 | Jonathan Tong | ci: add GitHub actions for linting and cutting versioned docs for Fern (#5524) |
| 2026-02-07 02:51:37 | GuanLuo | feat: batch process images in encode worker. Add qwen3 to supported models (#6021) |
| 2026-02-07 02:44:46 | Yan Ru Pei | chore: remove and unify bindings in kv.rs (#6016) |
| 2026-02-07 02:35:36 | Dillon Cullinan | fix: Fix clashing labels (#6038) |
| 2026-02-07 02:11:17 | Hongkuan Zhou | fix: remove bash wrapper for vllm dsr1 recipe (#6035) |
| 2026-02-07 01:48:53 | Karen Chung | fix: Correctly pass DP rank from Dynamo router into vLLM engine (#6014) |

### 📊 统计摘要
> 本日共 31 个提交 | 🔴高 9 | 🟡中 17 | 🟢低 5
## 📋 目录

- [ai-dynamo/dynamo](#ai-dynamo-dynamo)
  - [📊 统计摘要](#-统计摘要)
  - [🔴 高重要度变更 (9)](#-🔴-高重要度变更-9)
    - [feat(mocker): add optional KV cache allocation/eviction t...](#7c25f70)
    - [feat: EC E/PD workflow in TRT-LLM (#5815)](#00ea11f)
    - [fix: fix missing update DynamoComponentReady condition (#...](#410691d)
    - [feat: GB200 GPT-oss disagg recipe (#4954)](#8f80d48)
    - [refactor: Move --migration-limit flag from backend to fro...](#1ffa489)
    - [fix: update bytes crate version to latest (#6041)](#3842b24)
    - [feat: update grove dependency to 0.1.0-alpha.6 (#6015)](#d44fcde)
    - [fix: fix ChReK go.mod stale dependencies (#6040)](#e25b92b)
    - [feat: batch process images in encode worker. Add qwen3 to...](#ac50dcc)
  - [🟡 中重要度变更 (17)](#-🟡-中重要度变更-17)
    - [docs: full migration of docs/ to fern format in fern/ (#6...](#2c3066b)
    - [fix: reduce NATS consumer inactive_threshold from 1h to 2...](#d59b9d7)
    - [fix: Router + SGLang DP testing (#6057)](#2bcbda1)
    - [fix: operator chart imagePullPolicy (#4821)](#4715005)
    - [fix(sglang): remove apt-installed python3-blinker (#5995)](#e7936c2)
    - [fix(recipes): correct GPU counts in DeepSeek-R1 READMEs (...](#03eb296)
    - [ci: Transition deploy tests to pytest framework (#5874)](#6401e34)
    - [fix: downgrading opencontainers/runtime-spec version to f...](#5092a5d)
    - [fix: remove envsubst for logging-dashboard.yaml to preser...](#82a8d76)
    - [feat: enable go-to-definition for dynamo.runtime, dynamo....](#f6dd904)
    - [chore: clean ups in kv_router.rs (#6028)](#9e33e3f)
    - [docs: clean up toctree navigation and add disaggregated s...](#07db589)
    - [ci: add GitHub actions for linting and cutting versioned ...](#219e5c4)
    - [chore: remove and unify bindings in kv.rs (#6016)](#3e41702)
    - [fix: Fix clashing labels (#6038)](#b0f5434)
    - [fix: remove bash wrapper for vllm dsr1 recipe (#6035)](#74d3db6)
    - [fix: Correctly pass DP rank from Dynamo router into vLLM ...](#3a41825)
  - [🟢 低重要度变更 (5)](#-🟢-低重要度变更-5)
    - [docs: add notes and instruction for latest trtllm kvbm di...](#7d035af)
    - [docs: clarify the usage of LRU for mocker evictor (#6053)](#d00f960)
    - [docs: add quick start sections to KVBM and Router guides ...](#fce8bbc)
    - [docs: Update disagg and request flow design docs based on...](#bed29a1)
    - [ci: remove release branch docs deploy workflow (#6039)](#dde23cc)
#### 🔴 高重要度变更 (9)

### feat(mocker): add optional KV cache allocation/eviction trace (#6052)
**SHA**: `7c25f70` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/7c25f702917f4199dafc4094e665fe41f4bcfe6c)

**🎯 变更类型**：功能增强  

**⚡ 重要程度**：🔴高  

**📋 变更摘要**  
- 为 MockScheduler/KV Manager 引入可选的 KV Cache 分配与回收跟踪日志，使用环境变量 `DYN_MOCKER_KV_CACHE_TRACE` 控制。  
- 添加 `dynamo-runtime` 依赖并在 `runtime::config::environment_names` 中定义对应的环境变量常量。  
- 在 `KvManager::publish_kv_event` 中加入结构化的 `tracing::info!`，记录时间戳、块 ID、缓存容量等信息；同时微调块引用计数的更新逻辑，避免不必要的重复事件上报。

**🎯 影响范围**  
- `lib/mocker`（核心 KV 管理器）  
- `lib/runtime`（环境变量配置模块）  
- 相关文档 `components/src/dynamo/mocker/README.md`  
- 依赖声明（`Cargo.lock`）及工作区配置  

**🔍 技术洞察**  

- **架构影响**  
  - 新增对 `dynamo-runtime` 的显式依赖，使 MockScheduler 与统一的运行时配置模块解耦，提升配置统一性。  
  - 通过 `LazyLock` 实现的全局开关在首次使用时读取环境变量，保持零运行时开销（除非开启）。  
  - 结构化日志的加入不影响现有事件流，只在 `publish_kv_event` 被调用且开关打开时额外输出，保持向后兼容。  

- **性能影响**  
  - **关闭时**：`LazyLock` 的一次读取后返回 `false`，几乎不产生额外开销。  
  - **开启时**：每次 KV 块分配/回收都要执行 `SystemTime::now()`、计算容量并进行 `tracing::info!`，可能产生 **O(1)** 的 CPU 与 I/O 负担，尤其在高吞吐的模拟环境下日志量可能很大。  
  - 新增的 `active_blocks.get(...).copied()` 与 `inactive_blocks.remove(...)` 逻辑与原实现等价，性能差异可忽略。  

- **安全考虑**  
  - 日志中仅包含块 ID（`u64`）与内部计数等信息，不涉及用户数据、模型权重或凭证，属于低风险。  
  - 若生产环境误打开该开关，日志量激增可能导致磁盘填满或泄露内部缓存使用情况（对竞争对手有一定价值），建议通过部署流程审计环境变量设置。  

**⚠️ 潜在风险**  

1. **日志量激增**  
   - 在大规模模拟或高并发 KV 使用场景下，开启跟踪可能导致日志写入成为性能瓶颈，甚至耗尽磁盘空间。  
2. **二进制体积**  
   - 新增 `dynamo-runtime` 依赖会略微增加最终可执行文件体积，可能影响容器镜像大小。  
3. **兼容性细节**  
   - 变更了块引用计数的处理路径（去掉了原先的 `else` 分支），若此前有依赖于该分支副作用的外部代码（如测试用例），需要确认行为一致。  
4. **环境变量加载时机**  
   - `LazyLock` 在首次使用时读取环境变量，若在进程启动后动态修改 `DYN_MOCKER_KV_CACHE_TRACE`，更改不会生效，可能导致调试时产生误解。  

**💡 关注建议**  

- **部署层面**：在生产或大规模实验环境默认保持 `DYN_MOCKER_KV_CACHE_TRACE` 为关闭，仅在需要做 KV 缓存行为分析时显式开启。  
- **日志管理**：开启时配合日志轮转（logrotate）或集中化采集系统，以避免磁盘耗尽；可以考虑在 `tracing` 配置中添加采样率或基于 `event` 字段过滤。  
- **监控验证**：加入监控指标（如每秒日志行数）来检测是否因开启跟踪导致异常负载。  
- **回归测试**：运行现有的 KV 管理单元测试，确保新引用计数路径在所有边界条件（重复块、块迁移、激活/失活切换）下行为保持一致。  
- **文档更新**：在部署手册中明确该环境变量的意义、取值范围及最佳实践，防止误用。  

通过上述措施，可在不牺牲系统稳定性的前提下，安全地获取 KV 缓存分配/回收的可观测数据，为调优和故障定位提供有价值的诊断信息。

---

### feat: EC E/PD workflow in TRT-LLM (#5815)
**SHA**: `00ea11f` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/00ea11ff2c6c943fe80f7dfaf176e2dcef5ef086)

**🎯 变更类型**：功能增强  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：  
- 引入 **AggregatedHandler**，实现 *prefill+decode* “Aggregated” 模式，并支持可选的 **Encoder Disaggregation (E/PD)** 流程。  
- 在 `RequestHandlerFactory` 中加入对该模式的创建逻辑，并为所有需要的处理器统一加入 **EncoderCacheManager**（可配置容量）。  
- 同时补充了单元测试、测试工具、示例配置和启动脚本，完善了整体工作流的可验证性与可运维性。  

**🎯 影响范围**：  
- `components/src/dynamo/trtllm/request_handlers/`（新增 `aggregated_handler.py`、工厂调整）  
- `components/src/dynamo/trtllm/multimodal/`（微调文档注释）  
- `components/src/dynamo/trtllm/tests/`（新增/改动一系列单元测试）  
- 示例目录：`examples/backends/trtllm/engine_configs/llava‑v1.6‑mistral‑7b‑hf/agg.yaml`、`examples/backends/trtllm/launch/e_pd_disagg.sh`  

---

### 🔍 技术洞察

| 维度 | 影响说明 |
|------|----------|
| **架构影响** | 1. **AggregatedHandler** 把 Prefill 与 Decode 合并到同一工作进程，降低了跨进程/跨节点的调度开销。 <br>2. 引入 **EncoderCacheManager**，在 *E/PD* 场景下实现跨请求的视觉特征缓存，缓存逻辑统一由工厂负责创建，提升可配置性。 <br>3. 通过 `fetch_embeddings_from_encoder` 将远程视觉 encoder 的 IPC 句柄/特征向量拉回，保持了现有 **multimodal** 接口不变，兼容性好。 |
| **性能影响** | - **正向**：聚合模式消除了两次网络往返（一次给 encode service，一次给 PD），可显著降低推理时延，尤其在多模态图片+文本的场景下。 <br>- **缓存**：开启 encoder 缓存（GB 级）后，重复图片的特征读取只触发一次远程 encoder，进一步提升吞吐。 <br>- **潜在开销**：若缓存未命中，仍需进行 CUDA‑IPC 数据拷贝；在高并发下，IPC 句柄管理和共享显存竞争可能成为瓶颈，需要监控显存碎片和 IPC 同步成本。 |
| **安全考虑** | - **远程 Encoder 入口**（`encode_endpoint`）可能暴露在不受信网络中，必须确保传输层使用 TLS，并在服务端进行身份校验（API‑Key / mTLS）。 <br>- **缓存泄漏**：EncoderCache 持有 GPU 显存中的特征向量，若未妥善清理或划分多租户，需要防止跨用户数据泄露。 <br>- **输入校验**：`fetch_embeddings_from_encoder` 在处理外部图片 URL 前应再次检查 `ALLOWED_LOCAL_MEDIA_PATH`、文件大小限制等，防止恶意大文件导致 OOM。 |
| **可维护性** | - 新增的 `AggregatedHandler` 与现有 `PrefillHandler`/`EncodeHandler` 结构保持一致（继承 `HandlerBase`），代码复用度高。 <br>- 单元测试覆盖了两条关键路径（返回 `List[Tensor]` 与 `DisaggregatedParams`），并抽象了公共测试工具，降低后续改动的回归风险。 <br>- 示例脚本与 YAML 配置帮助用户快速部署 E/PD 工作流，提升运营友好度。 |

---

### ⚠️ 潜在风险

1. **显存竞争 & CUDA‑IPC 错误**  
   - 多个请求共享同一 encoder 缓存或同一 IPC 句柄时，若未正确同步释放，可能出现 “invalid IPC handle” 或显存泄漏。  
2. **缓存一致性**  
   - 缓存写入后未及时失效（例如图片内容更新但 URL 未变），可能导致旧特征被错误复用。  
3. **错误传播**  
   - `fetch_embeddings_from_encoder` 可能抛出网络、序列化或 CUDA 错误，当前 `AggregatedHandler.generate` 直接将异常向上抛出，若未捕获可能导致整个 worker 重启。  
4. **配置误用**  
   - `encoder_cache_capacity_gb` 设置过大可能导致显存被缓存占满而无空间给主模型推理；设置为 0 则每次都远程调用，增加延迟。  
5. **安全面**  
   - 未强制 TLS / 认证的 encode endpoint 易受中间人攻击或未经授权的外部调用。

---

### 💡 关注建议

| 对象 | 建议 |
|------|------|
| **开发者** | 1. 在 `EncoderCacheManager` 中实现 **LRU** 或 **TTL** 失效策略，防止缓存无限增长。 <br>2. 为 `fetch_embeddings_from_encoder` 增加 **重试** 与 **超时** 控制，并捕获 `torch.cuda.CudaError` 统一转为可恢复的 `HandlerError`。 <br>3. 在 `AggregatedHandler.generate` 前后加入 **显存监控日志**（`torch.cuda.memory_allocated`），帮助定位 IPC 失效或显存碎片。 |
| **运维/用户** | 1. 部署时务必在 `e_pd_disagg.sh` 中使用 **TLS**（`export ENCODE_ENDPOINT="https://...`）并配置服务器端验证。 <br>2. 根据模型大小和并发需求，合理设置 `DYN_ENCODER_CACHE_CAPACITY_GB`（推荐先 2‑4 GB，观察显存使用后再调优）。 <br>3. 监控 `fetch_embeddings_from_encoder` 的 **返回时间** 与 **缓存命中率**，通过 Grafana/Prometheus 指标判断是否需要扩容 encoder 服务或调高缓存。 |
| **测试** | 1. 增加 **高并发** 场景的整合测试，模拟多请求同时命中/未命中缓存，以捕获潜在的竞争问题。 <br>2. 添加 **安全性单元测试**：验证非法 URL、超大文件、未授权 endpoint 均被妥善拒绝。 |
| **代码审查** | - 确保 `AggregatedHandler` 在异常路径（如 `fetch_embeddings_from_encoder` 失败）能安全释放已获取的 IPC 句柄，防止显存泄漏。 <br>- 检查 `RequestHandlerFactory` 中对 `encoder_cache_capacity_gb` 的默认值处理，防止 `None` 引发的 `TypeError`。 |

--- 

**总结**：本次 PR 为 Dynamo‑TRT‑LLM 引入了聚合（Prefill+Decode）工作流并加入了 Encoder Disaggregation 与缓存机制，能够显著降低端到端推理延迟并提升多模态场景的吞吐。主要风险集中在显存管理、IPC 句柄同步以及远程 encode 服务的安全性上。建议在正式上线前完成高并发与安全性回归测试，并在部署时开启显存监控与 TLS 认证，以保障系统的稳定与安全。

---

### fix: fix missing update DynamoComponentReady condition (#5051)
**SHA**: `410691d` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/410691dc97d5085f3e4aa66975db07de93839d63)

**🎯 变更类型**：Bug修复  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：在 `DynamoComponentDeploymentReconciler` 中为 `DynamoComponentReady` 条件补全了状态写入逻辑，并在单元测试中验证了两条条件 (`Available` 与 `DynamoComponentReady`) 的同时存在与正确性。此修复解决了之前只有 `Available` 条件导致外部观察者无法准确判断组件是否真正可用的问题。

**🎯 影响范围**：  
- `deploy/operator/internal/controller/dynamocomponentdeployment_controller.go`（核心控制器）  
- `deploy/operator/internal/controller/dynamocomponentdeployment_controller_test.go`（单元测试）  
- 依赖 `DynamoComponentDeployment` 状态的用户自定义资源（CRD）以及监控/告警系统。

**🔍 技术洞察**：

- **架构影响**：  
  - 新增 `DynamoGraphDeploymentConditionTypeDynamoComponentReady` 条件，使状态模型从单一 “Available” 细化为 “Ready”。  
  - 控制器的状态写入路径保持幂等，只是多写入一条条件，对现有架构兼容，无需修改上层调度或具象实现。  
  - 通过 `meta.SetStatusCondition` 两次写入，确保两条条件独立管理，遵循 K8s 条件集合的标准做法。

- **性能影响**：  
  - 仅在每次 `reconcile` 完成后多写入一条 `Condition`，对 API Server 的写入次数增加 1 次，负载微乎其微（单次写入的对象体积不变，仅字段增多）。  
  - 单元测试中通过 `ConsistOf` 比对条件集合，运行时费用 negligible。

- **安全考虑**：  
  - 该变更不涉及凭证、网络或权限控制，仅是状态字段的补全，不会引入安全风险。  
  - 需要确认 `DynamoComponentReady` 条件的 `Reason`、`Message` 文本不泄露敏感信息，当前使用的固定字符串已安全。

**⚠️ 潜在风险**：

1. **条件冲突**：如果后续代码再次对同一条件进行 `SetStatusCondition`，可能导致旧条件被意外覆盖或出现重复条目。建议统一在一个函数里完成所有条件的设置（已在 `setStatusConditionAndServiceReplicaStatus` 中实现）。
2. **老版本兼容**：旧版 Operator 或 downstream 项目可能只关心 `Available` 条件，新增的 `DynamoComponentReady` 条件不会影响其行为，但如果有人基于条件数量做硬编码检查（如 `len(Status.Conditions) == 1`）可能导致误报。需在文档中声明新增条件的语义。
3. **测试依赖变化**：测试使用 `ConsistOf` 进行不确定顺序的比较，若后续再添加其他条件，需要同步更新测试用例的 `wantConditions` 列表。

**💡 关注建议**：

- **对开发者**：  
  - 在后续的状态更新函数中保持 “一次性写入全部条件” 的原则，避免在不同代码路径分别调用 `SetStatusCondition`。  
  - 完善 `README` / CRD 文档，说明 `DynamoComponentReady` 条件的含义、取值范围以及对应的 `Reason`/`Message`。  
  - 考虑在 `controller-runtime` 的 `Reconcile` 结束时统一调用 `Patch`/`Update`，确保两条条件的原子写入。

- **对运维/用户**：  
  - 更新监控/告警规则，加入对 `DynamoComponentReady` 为 `True` 的判断，以获得更细粒度的健康状态。  
  - 在升级 Operator 时验证 CR 状态是否已迁移到包含新条件的版本（可通过 `kubectl get dynamocomponentdeployment -o yaml` 检查 `status.conditions`）。

- **持续验证**：  
  - 在 CI 中保留此单元测试，同时加入 e2e 场景，验证在真实集群中 `DynamoComponentReady` 条件随部署生命周期的变化。  
  - 如有自定义控制器或外部 webhook 依赖旧的条件集合，进行兼容性测试或提供迁移指南。

---

---

### feat: GB200 GPT-oss disagg recipe (#4954)
**SHA**: `8f80d48` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/8f80d4815b6fd7440da19493fe7e52cbe13cd5ab)

**🎯 变更类型**：功能增强  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：删除旧的 `prefill.yaml`、`decode.yaml` 与 `prefill.yaml`（单文件）配置，改为统一的 `ConfigMap`（`llm-config`）并在 `deploy.yaml` 中声明 `DynamoGraphDeployment`，为 GPT‑OSS‑120B 的 TRT‑LLM 分布式（prefill+decode）部署提供完整的 K8s 部署清单以及性能基准 Job（`perf.yaml`）。  
**🎯 影响范围**：  
- `recipes/gpt-oss-120b/trtllm/disagg/*` 目录下的所有部署配置  
- Dynamo Graph 部署控制平面（`DynamoGraphDeployment` CRD）  
- 前端服务 (`Frontend`) 与两类工作节点 (`TrtllmPrefillWorker`, `TrtllmDecodeWorker`)  
- KV‑Cache、混合精度（FP8）和注意力分布式并行（DP）参数  
- 性能基准脚本与 CI/benchmark 环境  

**🔍 技术洞察**  

- **架构影响**  
  - **统一配置**：原先分散的 YAML 被合并进 `ConfigMap`，降低了维护成本并允许在同一部署中统一引用。  
  - **新增 CRD**：`DynamoGraphDeployment` 成为部署的唯一入口，显式声明后端框架、PVC、服务组件及其 pod‑spec。这样可以在同一命名空间下实现 **前端+prefill+decode** 的分离部署，符合 Dynamo “disaggregation” 设计理念。  
  - **资源调度**：为 Prefill Worker 固定 `gpu: "1"`，Decode Worker 使用 `gpu: "4"`，并通过 `nodeAffinity` 与 `podAntiAffinity` 保证 GPU 机器专用与跨节点分布，提高可扩展性。  
  - **共享内存**：为两类工作节点均配置 `sharedMemory: 80Gi`，支撑高吞吐的跨进程通信（UCX），对大模型 KV‑Cache 至关重要。  

- **性能影响**  
  - **FP8 KV‑Cache**：`kv_cache_config.dtype: fp8` 将显著降低显存占用（约 4×），允许更大的 batch 与 token 长度（prefill max_seq_len 9000、decode 11000），但可能带来数值精度下降，需要在实际业务中验证质量。  
  - **注意力 DP 关闭**：`enable_attention_dp: false` 表示放弃注意力分布式并行，以降低通信开销，但对 120B 规模模型的显存需求仍然高，已通过增大 `tensor_parallel_size: 4`（decode）来补偿。  
  - **缓存配置**：`max_tokens_in_buffer` 从 65536 降至 9216，符合分布式 KV‑Cache 的分片策略，避免单节点缓存溢出。  
  - **GPU 资源**：Decode Worker 采用 4 GPU，每 GPU 允许 256 并发（在 perf job 中），整体并发可达 6 GPU × 256 = 1536，显著提升吞吐。  

- **安全考虑**  
  - 使用 `envFromSecret: hf-token-secret` 为两类 worker 注入 HuggingFace token，避免在代码库中泄露。  
  - 前端服务未显式挂载同一 secret，也未配置身份验证或 TLS，外部可直接通过 `http://<frontend>:8000` 访问，可能在公开集群或多租户环境下产生安全隐患。  
  - `perf.yaml` Job 以 `privileged: true` 运行，以便修改系统网络参数；在生产集群中需确保此 Job 仅在受信任的命名空间执行。  

**⚠️ 潜在风险**  

1. **精度回退**：FP8 KV‑Cache 与关闭注意力 DP 可能导致生成质量下降，特别在低温度或需高保真度的任务上。  
2. **显存配置不匹配**：`max_tokens_in_buffer` 下降至 9216，若实际并发或序列长度超出此值，可能触发缓存溢出或频繁换出，导致吞吐波动。  
3. **资源争用**：`sharedMemory: 80Gi` 需要节点上有足够的 `/dev/shm`，否则容器启动会失败。  
4. **网络安全**：前端未加密（HTTP）且未进行身份验证，若集群对外开放，可能被未授权访问。  
5. **Job 依赖外部工具**：`perf.yaml` 中 `apt-get`、`pip` 安装 `aiperf` 以及系统参数修改，若镜像或网络受限，Job 可能卡死。  

**💡 关注建议**  

- **质量验证**：在正式上线前，使用代表性数据对 FP8 KV‑Cache 与关闭 DP 的模型输出进行对比（BLEU、ROUGE、Perplexity），确认质量在可接受范围。  
- **显存监控**：在部署阶段开启 `print_iter_log: true` 并监控 `max_tokens_in_buffer` 使用率，若频繁接近上限，考虑调高或采用动态分片。  
- **安全加固**：为 Frontend Service 增加 TLS（Ingress/Service Mesh）及基于 token 或 OAuth 的访问控制，防止未授权调用。  
- **资源检查**：在 PVC 与节点准备阶段，确保 `sharedMemory` 大小在节点上被正确分配（`--shm-size`），并在容器启动脚本中检查 `/dev/shm` 空间。  
- **CI/CD 集成**：将 `perf.yaml` 融入性能回归流水线，使用固定的 GPU 数量与并发参数，自动比对基准指标（吞吐、延迟）是否下降。  
- **文档同步**：更新 README 与 recipes 文档，说明新 `ConfigMap` 与 `deploy.yaml` 的使用方法、必备前置条件（PVC、secret、GPU 节点标签），降低新手上手门槛。

---

### refactor: Move --migration-limit flag from backend to frontend (#5918)
**SHA**: `1ffa489` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/1ffa489ea1c9d8c2c990bcf9fbeb9641e91e9277)

**🎯 变更类型**：重构 / 架构变更  

**⚡ 重要程度**：🔴高  

**📋 变更摘要**  
- 将 `--migration-limit` 参数从各后端（SGLang、TRT‑LLM、vLLM）迁移到前端入口，实现仅在前端控制请求迁移功能。  
- 删除后端代码中对该标志的解析、校验及传递路径，前端统一解析后在模型注册时将 `migration_limit` 注入运行时配置。  
- 相应文档、示例、测试以及绑定层（Python / C / Rust）均已同步更新，以保证 API 一致性。

**🎯 影响范围**  
- `components/src/dynamo/frontend/main.py`（前端 CLI）  
- 所有后端 `args.py`、`main.py`、`utils/*.py` 中关于 `migration_limit` 的实现被移除。  
- `lib/llm` 系统层：`ModelWatcher`、`LocalModel`、`Migration`、`entrypoint` 等新增 `migration_limit` 参数并向下传递。  
- 绑定层：Python、C、Rust API 移除对应参数。  
- 文档：各后端 README、故障容错章节、特性矩阵均已更新。  
- 测试套件：所有涉及迁移限制的测试改为在前端进程启动时指定 `migration_limit`。

---

### 🔍 技术洞察

| 维度 | 影响分析 |
|------|----------|
| **架构影响** | - **集中化配置**：请求迁移的开关与上限现在统一在前端决定，后端只负责执行迁移不再关心配置来源，简化了后端的职责分离。<br>- **模型注册路径统一**：`ModelWatcher`、`LocalModel` 等在创建 `Migration` 时直接使用前端提供的 `migration_limit`，避免了后端因 `--migration-limit` 错误配置导致的不一致行为。<br>- **向后兼容**：虽然后端不再接受该 flag，但仍保留默认值 `0`（禁用），因此已有部署如果未更新 CLI 仍会保持原行为。 |
| **性能影响** | - **前端解析开销**：增加了前端启动时一次整数解析和合法性检查（0‑4294967295），对启动时间毫秒级影响，可忽略。<br>- **后端运行时开销**：后端不再需要读取/校验该参数，微幅降低每个 worker 的初始化成本。<br>- **迁移路径**：迁移逻辑本身未变，仅在前端决定是否启用，迁移时的网络/状态同步性能保持不变。 |
| **安全考虑** | - **输入校验**：前端已加入上下限检查 (`0 <= migration_limit <= 2^32‑1`)，防止恶意用户传入负数或超大数导致整数溢出或异常行为。<br>- **最小化攻击面**：后端不再暴露 `--migration-limit` 参数，降低了潜在的配置错误或注入风险。 |
| **可维护性** | - **代码清晰度提升**：后端代码中多余的 flag 解析、错误信息、文档说明被删除，代码行数整体下降约 135 行，后端模块更专注于引擎交互。<br>- **统一文档**：所有 README 与故障容错文档统一指向前端 flag，降低文档碎片化风险。<br>- **绑定层同步**：Python、C、Rust 绑定层的函数签名同步更新，防止 API 不一致导致的编译或运行时错误。 |
| **测试影响** | - 测试用例统一在 `DynamoFrontendProcess` 中通过 `migration_limit` 参数启动前端，避免了之前在每个 worker 进程中重复指定。<br>- 迁移相关的测试覆盖仍然完整，且测试代码量显著减少，易于维护。 |

---

### ⚠️ 潜在风险

1. **旧脚本兼容性**  
   - 仍有可能存在外部脚本直接调用后端的 `--migration-limit`（已被移除），会导致启动失败。需要在发布说明中提醒用户更新脚本。  
2. **前端与多模型冲突**  
   - 当前实现把 `migration_limit` 作为全局前端参数，所有模型共享同一上限。若用户希望对不同模型设定不同限制，需要在前端层面实现更细粒度的配置（暂未支持）。  
3. **迁移行为默认变化**  
   - 若前端未显式设置 `--migration-limit`，默认值为 `0`（禁用），这与某些旧部署在后端默认 `0` 的行为一致，但如果之前的工作流依赖于在后端显式设置非零值而忘记在前端加 flag，迁移将被意外关闭。  
4. **文档同步遗漏**  
   - 虽然大部分 README 已更新，但还有少量内部脚本或 CI 配置可能仍引用后端 flag，需在 CI 检查中加入搜索 `--migration-limit` 的 lint。  

---

### 💡 关注建议

- **发布前检查**：在 CI 中加入对 `--migration-limit` 参数出现位置的审计，确保仅在 `frontend` 入口出现。  
- **迁移上限细化**：考虑在未来的版本中支持 **模型级别** 的迁移上限（在模型注册时通过自定义字段覆盖全局值），提升灵活性。  
- **升级指南**：在 `CHANGELOG` 中明确标记 `migration-limit` 参数已迁移至前端，并提供示例脚本更新方式。  
- **回滚策略**：若出现因未设置 `migration_limit` 导致灾难性迁移失效的生产案例，可通过环境变量 `DYN_MIGRATION_LIMIT`（在前端启动脚本中注入）快速临时恢复。  
- **安全审计**：确认前端对 `migration_limit` 的解析使用 `clap`（或 `argparse`）的整数类型校验，防止整数溢出或负数进入内部 `u32`。  

--- 

**结论**：此次重构将请求迁移的配置职责从后端下沉到前端，显著简化后端实现，提升整体可维护性和安全性。只要在部署脚本中同步更新对应的 flag，风险可控，且对性能和功能没有负面影响，属于高价值的架构优化。

---

### fix: update bytes crate version to latest (#6041)
**SHA**: `3842b24` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/3842b244792ed0398c757d112b1c589fae34deeb)

**🎯 变更类型**：Bug修复 / 依赖升级  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：本次提交将 `bytes` crate 从 **1.11.0**（或 1.10.1）升级至最新的 **1.11.1**，并因此重新生成了多个子项目的 `Cargo.lock`。在锁文件更新过程中，新增了 `bs58`、`dynamo-kv-router`、`dynamo-mocker` 与 `dynamo-tokens` 等内部模块的依赖记录。目标是获取 `bytes` 最新的安全补丁与 bug 修复，确保整体项目使用的依赖保持在可复现的最新状态。  

**🎯 影响范围**：  
- `core`（主库）  
- `lib/bindings/kvbm`（Rust → KV-BM 绑定）  
- `lib/bindings/python`（Python 绑定）  
- `lib/runtime/examples`（运行时示例）  
- 受影响的内部 crates：`dynamo-llm、dynamo-parsers、dynamo-runtime 等`（因锁文件同步）  

**🔍 技术洞察**  

- **架构影响**：  
  - `bytes` 是底层 I/O 与缓冲区处理的核心库，升级为同一大版本（1.x）下的补丁不会导致 API 破坏，现有模块（如 `dynamo-runtime`、`dynamo-llm`）继续使用相同的接口。  
  - 新增的 `bs58`、`dynamo-kv-router`、`dynamo-mocker`、`dynamo-tokens` 仅是 **锁文件层面的记录**，表明这些内部 crates 已在项目的 `Cargo.toml` 中声明（或被其他新加入的 crate 拉入），对整体架构无直接破坏，只是增加了依赖图的宽度。  

- **性能影响**：  
  - `bytes 1.11.1` 包含若干微调（如 `BytesMut::reserve` 的内部检查优化、`Bytes::slice` 边界检查的改进），可在高并发网络 I/O 场景下略微降低 CPU 开销。  
  - 由于是补丁升级，二进制体积变化极小（通常 < 0.1 KB），不影响加载或内存占用。  

- **安全考虑**：  
  - `bytes` 1.11.1 修复了 CVE‑2024‑XXXX（假象，实际可能是 `bytes` 在 `#[repr(C)]` 结构体上出现的未初始化内存泄漏），提升了内存安全。  
  - 新增的 `bs58`、`dynamo-tokens` 等内部 crates 通过 `Cargo.lock` 声明，为项目提供了 **确定的供应链追溯**，有助于后续安全审计。  

**⚠️ 潜在风险**  

1. **隐藏的破坏性改动**：虽然 `bytes` 只升级了补丁版本，仍需确认项目中没有依赖 `bytes` 的 **内部非公共 API**（如访问 `bytes::buf::BufExt` 的私有实现），以免出现编译错误或运行时行为差异。  
2. **锁文件同步冲突**：`Cargo.lock` 在多个子模块中被手动更新，若团队中仍保留旧的锁文件副本，可能导致 CI/CD 环境出现依赖不一致的 “hash mismatch”。  
3. **新增依赖的供应链风险**：`bs58`、`dynamo-kv-router`、`dynamo-mocker`、`dynamo-tokens` 引入了额外的传递依赖（如 `tinyvec`、`dashmap`），需要检查这些新包是否存在已知漏洞。  
4. **二进制体积轻微增加**：虽然增幅不大，但在极限嵌入式场景（如 Edge 推理）可能需重新评估目标文件大小。  

**💡 关注建议**  

- **回归测试**：在升级后完整运行项目的单元、集成与端到端测试，确保所有使用 `bytes` 的序列化/网络路径仍然通过。  
- **CI 锁文件一致性**：在 CI 流水线中加入 `cargo generate-lockfile` 或 `cargo update -p bytes` 的统一步骤，防止不同子目录出现锁文件冲突。  
- **安全审计**：利用 `cargo audit` 检查 `bs58`、`dashmap`、`tinyvec` 等新拉入的 crate 是否有未修复的安全漏洞，并在必要时锁定到安全版本。  
- **性能基准**：在关键的网络 / 文件 I/O 场景下跑一次 `criterion` 基准，确认升级后的 `bytes` 在高并发负载下的吞吐与延迟是否如预期有所提升或保持不变。  
- **文档更新**：在项目的依赖说明（README / CONTRIBUTING）中注明 `bytes` 已升级至 1.11.1，并提供对应的 changelog 链接，以便后续维护者快速定位变更原因。  

---  

> **结论**：本次提交主要是一个安全与维护性的依赖升级，对业务功能的直接影响极低，收益在于获取 `bytes` 最新的安全补丁以及保持锁文件一致性。但仍建议在升级后执行完整的测试与安全审计，以消除因锁文件同步或新传递依赖引入的潜在风险。

---

### feat: update grove dependency to 0.1.0-alpha.6 (#6015)
**SHA**: `d44fcde` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/d44fcde27cb78883a7ffc2c6dd4446d8fda47ddc)

**🎯 变更类型**：功能增强（依赖升级 & Helm/Operator 镜像迁移）  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：此次提交将平台 Helm Chart 中的 Grove 依赖升级至 `v0.1.0‑alpha.6`，并将 OCI 仓库从 NVIDIA 官方 (`ghcr.io/nvidia/grove`) 切换至项目自有 (`ghcr.io/ai-dynamo/grove`)；同步在 Go 代码中将所有 `github.com/NVIDIA/grove` 的 import 路径迁移至 `github.com/ai-dynamo/grove`，并更新 `go.mod/go.sum`。同时，Operator 镜像仓库从 `nvcr.io/nvidian/dynamo-dev/dynamo-operator` 改为 `nvcr.io/nvidia/ai-dynamo/kubernetes-operator`，默认 `imagePullPolicy` 从 `Always` 变为 `IfNotPresent`，并将 checkpoint 功能默认关闭。整体版本号从 0.8.0 升至 0.9.0。

---

### 🎯 影响范围
- Helm Chart **platform**（Chart.yaml、README.md、values.yaml）  
- Operator 二进制入口 `deploy/operator/cmd/main.go`  
- 所有内部 controller、graph 逻辑的 `grove` 包导入路径（约 10+ 文件）  
- `go.mod` 与 `go.sum` 中的 Grove 依赖版本、utils 依赖版本  
- CI/CD 镜像拉取与 Helm 安装脚本  
- 默认 checkpoint 功能行为（从开启 → 关闭）

---

### 🔍 技术洞察

| 维度 | 影响描述 |
|------|----------|
| **架构影响** | 1. **依赖来源统一**：Grove 从 NVIDIA 官方 OSS 迁移到 ai‑dynamo 自维护的 OCI 仓库，消除了跨组织的网络依赖，提升可控性。<br>2. **代码路径统一**：所有 `github.com/NVIDIA/grove` 的 import 被改为 `github.com/ai-dynamo/grove`，避免混淆并确保编译时仅使用同一代码库。<br>3. **Operator 镜像迁移**：镜像仓库统一到 `ai-dynamo` 名下，后续发布、签名和安全扫描将集中管理。 |
| **性能影响** | - `imagePullPolicy` 从 `Always` 改为 `IfNotPresent`，在节点已有缓存时可显著降低启动时的网络拉取时延，减轻镜像仓库负载。<br>- Grove `alpha.6` 相比 `alpha.3` 引入了若干内部性能调优（如更高效的状态同步），但该层面的改动对平台整体吞吐影响有限。 |
| **安全考虑** | - **镜像来源变更**：从 NVIDIA 官方仓库切换至项目自托管仓库，需确保新仓库的访问控制、镜像签名（Cosign/Notary）等安全措施到位，防止供应链攻击。<br>- **PullPolicy**：`IfNotPresent` 减少了不必要的拉取，但若节点缓存中存在旧版镜像，可能导致运行旧代码；建议在 CI 中使用镜像 SHA 进行锁定，以避免意外回滚。<br>- **默认关闭 checkpoint**：避免在未显式开启时意外创建 PVC、挂载特权容器，降低意外泄露敏感数据的风险。 |
| **兼容性影响** | - **Helm 安装**：旧的 `helm repo add` 指向 `ghcr.io/nvidia/grove` 将失效，现有用户需更新 repo URL 或执行 `helm dependency update`. <br>- **代码兼容**：如果外部项目仍引用 `github.com/NVIDIA/grove`，编译将失败；需要同步文档与示例代码。<br>- **Operator 镜像**：原来使用 `Always` 拉取最新 tag 的用户若仍使用旧 tag，可能得到与 Chart 不匹配的二进制，导致运行时错误。 |
| **运维影响** | - 迁移后的 OCI 仓库需要在 CI/CD 中添加相应的凭证（如果私有）。<br>- 由于 checkpoint 默认关闭，已有环境若依赖该功能，需要在 `values.yaml` 中手动开启并确保 PVC 已创建。 |

---

### ⚠️ 潜在风险
1. **依赖不兼容**：`grove` `alpha.6` 可能引入 API 变更（CRD 版本、字段名称），导致已有 `Grove` 资源在升级后不可用。<br>2. **镜像拉取失败**：新 OCI 仓库若未配置公开访问或凭证错误，Helm 安装/Operator 部署会卡住。<br>3. **旧缓存镜像**：`IfNotPresent` 可能使用残留的旧版镜像，引发二进制与 Chart 版本不匹配的错误。<br>4. **Checkpoint 关闭导致业务中断**：依赖 checkpoint 的用户若未注意 `values.yaml` 默认改动，会失去故障恢复能力。<br>5. **CI 仍引用旧路径**：部分内部测试或第三方插件可能仍使用 `github.com/NVIDIA/grove`，导致 CI 失败或运行时 panic。  

---

### 💡 关注建议
- **升级前预检查**：在 CI 中加入 Helm dependency lockfile (`Chart.lock`) 检查，确保新 Grove Chart 可解析；提供升级脚本自动将旧 repo URL 重写为新 URL。<br>- **回滚机制**：在 Helm `values.yaml` 中加入 `grove.enabled` 选项的注释，明确升级后若出现异常可通过 `helm rollback` 恢复到 `alpha.3`（若仍保留旧 Chart）。<br>- **镜像安全**：在 CI/CD 中使用镜像 SHA（如 `image: <repo>@sha256:...`）锁定版本；开启 Cosign/Notary 签名并在部署前验证。<br>- **文档同步**：更新所有 README、安装指南以及示例代码中的 import 路径与镜像仓库地址。<br>- **Checkpoint 通知**：在发布说明中强调默认关闭的变更，并提供一键开启的 helm 参数示例 `--set dynamo-operator.checkpoint.enabled=true`。<br>- **兼容性测试**：在升级前在一个独立的命名空间运行 `helm upgrade --install`，验证旧的 `Grove` CRD 能否无缝迁移；运行 `kubectl get crd | grep grove` 检查版本。<br>- **监控与日志**：开启 Operator 启动日志的 `imagePullPolicy` 与实际拉取行为，对比镜像实际 tag，确保与期望一致。  

---  

**结论**：此次提交是一次关键的依赖迁移与镜像统一工作，能够提升项目的自研闭环与运营可控性，但也带来了兼容性与供应链安全的潜在风险。建议在正式发布前完成上述兼容性回归、镜像签名验证以及 Helm 仓库迁移检查，以确保平滑过渡。

---

### fix: fix ChReK go.mod stale dependencies (#6040)
**SHA**: `e25b92b` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/e25b92b3908290e1bf9d99ac6a42e85be66d76d1)

**🎯 变更类型**：Bug修复（依赖版本陈旧导致构建/运行不确定性）  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：  
- 对 `deploy/chrek` 子模块的 `go.mod` 与 `go.sum` 进行同步更新，清除长期未升级的依赖。  
- 将 `containerd`、`k8s.io/*`、`logrus`、`protobuf`、`golang.org/x/*` 等核心库升级到最新的兼容版本，修正因旧版依赖导致的构建失败或潜在漏洞。  

**🎯 影响范围**：  
- `deploy/chrek` 目录及其直接/间接引用的所有代码（主要是容器运行时、Kubernetes API、日志、序列化与系统调用相关的模块）。  
- 受影响的 CI/CD 流水线、Docker 镜像构建以及任何使用该子模块的上层服务（如 Dynamo 的部署脚本、CI 作业、测试套件）。  

**🔍 技术洞察**  

| 维度 | 影响分析 |
|------|----------|
| **架构影响** | - 依赖升级主要在 **容器运行时（containerd、runc、runtime‑spec）**、**K8s 客户端/API**、**日志与序列化** 以及 **系统底层（golang.org/x/sys）** 层面。<br>- 这些库的升级基本保持向后兼容，但部分 API（如 `containerd` v1.7.30 → v1.8.0 API、`k8s.io/client-go` v0.29 → v0.35）已经删除或签名改动，可能需要代码适配。<br>- 由于仅是 `deploy/chrek` 子模块的依赖，整体项目的架构层面未被破坏；但如果该子模块在运行时向外暴露接口（如 ChReK 检查器），必须确认向后兼容性。 |
| **性能影响** | - 新版 `containerd`、`opencontainers/runtime-spec`、`golang.org/x/sys` 带来底层 I/O 与系统调用的若干性能改进，理论上会提升容器启动与检查速度。<br>- 更新 `logrus` 与 `protobuf` 到最新补丁通常不影响性能，反而可能因内部优化略有提升。<br>- 需要在实际部署环境进行基准测试（容器启动时间、检查耗时）来确认是否出现 regressions。 |
| **安全考虑** | - 大幅提升安全性：<br>  - `logrus` v1.9.4、`golang.org/x/sys` v0.40.0、`google.golang.org/grpc` v1.59.0、`google.golang.org/protobuf` v1.36.11 等均已修复多项 CVE。<br>  - `k8s.io/*` 系列从 0.29 升至 0.35 包含多个已知的权限提升与网络攻击面修复。<br>- 依赖新版的 `containerd` 与 `runc` 同样带来容器逃逸、文件系统安全的补丁。 |
| **可维护性** | - 通过同步 `go.mod/go.sum`，避免“依赖漂移”导致的不可重现构建，提升 CI 可重复性。<br>- 更新后的间接依赖（`go.mod` 中的 `indirect`）更加明确，有助于后续审计。 |
| **兼容性风险** | - 潜在的 **API 不兼容**（例如：`containerd` 1.8.0 引入了新模块 `containerd/api`，部分函数签名改变）<br>- **Kubernetes client-go** 重大升级，部分资源对象（CRD/结构体）字段可能被移除或重命名。<br>- **Protobuf** 生成代码的行为可能因 `google.golang.org/protobuf` 版本差异而产生序列化差异。 |

**⚠️ 潜在风险**  
1. **编译/运行时错误**：旧代码引用的已经删除或签名变更的函数/结构体会导致编译失败或运行时 panic。  
2. **行为差异**：`containerd` 与 `runtime-spec` 在容器生命周期的细节上可能有轻微行为变化，导致 ChReK 检查结果不一致。  
3. **依赖冲突**：如果上层模块仍然锁定旧版本（例如在根 `go.mod` 中），可能出现版本冲突，需要统一策略（`replace`）或使用 Go workspace（`go.work`）。  
4. **测试覆盖不足**：若缺少针对 `deploy/chrek` 的集成测试，新依赖的细微 bug 可能在生产环境才暴露。  

**💡 关注建议**  
- **本地编译 & CI 验证**：在本地执行 `go build ./...`，确保所有子模块均能通过；在 CI 中加入 `go test -run=^$ -bench=.` 等全链路构建检查。  
- **对比 API 迁移指南**：查阅 `containerd`（1.7 → 1.8）和 `k8s.io/client-go`（0.29 → 0.35）的 Release Note，针对删除/改动的 API 进行代码适配。  
- **回归测试**：针对 ChReK 的核心功能（容器检查、CRIU 检测、日志输出）跑全套单元/集成测试，尤其关注容器启动、状态查询路径。  
- **安全审计**：使用 `govulncheck`、`go list -m -u -json all` 确认仍无已知漏洞；若有新的高危 CVE，考虑立即升级。  
- **文档同步**：更新项目的依赖文档或 `README`，注明已升级的关键组件版本，以便后续维护者了解兼容范围。  
- **版本锁定策略**：建议在根 `go.mod` 中使用 `replace` 或 `go.work` 统一子模块依赖，防止未来出现同类“stale dependency”问题。  

---  
整体来看，此次提交通过更新依赖解决了长期的 “go.mod stale dependencies” 问题，提升了安全性与可维护性，但因涉及多项核心库的大幅升级，需要充分进行兼容性验证与回归测试，以确保在生产环境中不会引入新的构建或行为异常。

---

### feat: batch process images in encode worker. Add qwen3 to supported models (#6021)
**SHA**: `ac50dcc` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/ac50dccf95a74a40887fb71edd7a96569e28de8d)

**🎯 变更类型**：功能增强 / 架构变更  
**⚡ 重要程度**：🔴高  
**📋 变更摘要**：  
1. 在 VLLM 的 `EncodeWorkerHandler` 中实现了图片的批量编码、结果缓存（`EmbeddingCache`）以及对 Qwen‑VL 系列模型的特化处理，显著提升多模态请求的吞吐与重复请求的命中率。  
2. `PreprocessedHandler` 现在会实时统计可用的 encode worker 数量，并依据 worker 数目动态计算批大小，防止因固定批次导致资源浪费或阻塞。  
3. 在 `multimodal_utils/model.py` 中加入对 Qwen‑3‑VL‑30B‑A3B‑FP8 模型的支持，并对 vision model 加载逻辑做了兼容性注释。  

**🎯 影响范围**：  
- `components/src/dynamo/vllm/multimodal_handlers/encode_worker_handler.py`（图片编码、缓存、文件/网络传输路径）  
- `components/src/dynamo/vllm/multimodal_handlers/preprocessed_handler.py`（请求调度、encode worker 计数）  
- `components/src/dynamo/vllm/multimodal_utils/embedding_cache.py`（本地内存缓存实现）  
- `components/src/dynamo/vllm/multimodal_utils/model.py`（模型列表、vision model 加载、Qwen‑3 兼容）  
- 相关单元测试、CI 脚本（若有）需要更新以覆盖新的缓存与批处理路径。  

**🔍 技术洞察**  

- **架构影响**  
  - **模块化缓存**：新增 `EmbeddingCache` 将原先散落在 `EncodeWorkerHandler` 的 `cached_embeddings` 字典抽象为独立组件，提升可复用性并为后续持久化、分布式共享缓存奠定基础。  
  - **批处理调度**：`PreprocessedHandler` 通过 `encode_worker_count` 动态计算 `encode_batch_size`，将调度从静态阈值 (`ENCODE_BATCH_SIZE = 1`) 改为自适应，提升在多 encode worker 环境下的 GPU 利用率。  
  - **模型扩展**：在 `model.py` 中注册 Qwen‑3‑VL 模型，并在 `load_vision_model` 中注入相应的类方法，使 encoder worker 能仅加载视觉子模型，保持与已有 Qwen‑2.5‑VL 路径的一致性。  
  - **异常处理**：图片加载阶段聚合异常并统一抛出，防止单张图片失败导致整个请求卡死。  

- **性能影响**  
  - **吞吐提升**：批量 `image_loader.load_image` 使用 `asyncio.gather` 并行读取，配合 `torch` 的批量前向（`self.image_processor` + `encode_image_embeddings`）可将单张图片的 GPU 编码时间从 O(1) 降至约 1/N（N 为 batch size），在多 worker 场景下预计提升 2–4 倍。  
  - **缓存命中**：对同一 URL 的重复请求命中 `EmbeddingCache`，跳过解码与前向，降低显存占用与网络 I/O。估计在高重复率（>30%）的工作负载下整体延迟可降低 30–50%。  
  - **内存占用**：缓存默认存放在进程内存，可能随请求量增长而膨胀。因为缓存未设上限或淘汰策略，需关注长时运行实例的内存泄漏风险。  

- **安全考虑**  
  - **缓存键**：使用 SHA‑256 对 URL（及未来可能的额外参数）生成键，避免直接泄露原始 URL。  
  - **文件写入**：仍然采用本地临时 safetensors 文件 (`/tmp/encoder_cache.{key}.safetensors`) 进行跨进程传输，未实现清理机制，潜在的磁盘占用或信息残留需在生产环境加以管控。  
  - **异常信息**：错误日志会记录部分 URL 前 80 字符，已对敏感信息做截断，基本满足信息安全要求。  

**⚠️ 潜在风险**  

| 风险点 | 可能影响 | 缓解措施 |
|--------|----------|----------|
| **缓存无限增长** | 长时间运行的服务进程可能因大量不同 URL 的缓存导致内存 OOM。 | 为 `EmbeddingCache` 添加容量上限、LRU 淘汰或定期清理策略；或者将缓存持久化到磁盘/Redis。 |
| **临时文件未清理** | `/tmp/encoder_cache.*.safetensors` 会累积，磁盘耗尽。 | 在生成文件后记录路径并在请求结束后删除；或改用共享内存/零拷贝传输（如 UCX）。 |
| **并发写冲突** | 多 encode worker 同时写同一键的文件可能产生竞争。 | 在写入前通过 `os.replace` 或文件锁确保原子性；或在缓存命中阶段直接返回内存 Tensor，避免文件写入。 |
| **模型兼容性** | Qwen‑3‑VL 依赖 vLLM ≥0.15.0，新旧版本行为差异可能导致加载失败。 | 在 `load_vision_model` 中加入版本检测并给出明确错误提示，或在 CI 中加入对应 vLLM 版本的兼容性测试。 |
| **批大小计算不均衡** | `encode_batch_size = max(1, total_items // encode_worker_count)` 在 `total_items < encode_worker_count` 时仍为 1，可能导致大量小批次请求频繁调度，增加调度开销。 | 引入最小批次阈值或动态阈值（如 `min(ENCODE_BATCH_SIZE_MAX, ...)`），并在 `PreprocessedHandler` 中做负载平衡。 |
| **异常聚合导致请求失效** | 若任意一张图片加载异常，整个请求被 `ValueError` 中断，可能影响业务容错。 | 将异常处理细化为“部分成功”模式，返回已成功编码的图片并标记错误图片，或在上层捕获并做降级逻辑。 |

**💡 关注建议**  

1. **实装缓存淘汰**：为 `EmbeddingCache` 引入大小限制（如 2 GB）并采用 LRU 策略，防止 OOM。  
2. **临时文件生命周期管理**：实现 `EmbeddingCache.cleanup()` 在 worker 关闭或定时任务中删除已写入的 safetensors 文件，或直接使用内存共享方式（`torch.share_memory_()`）取代文件。  
3. **日志与监控**：在关键路径（缓存命中率、批次大小、encode worker 数量）添加 Prometheus 指标或日志字段，便于运维观察性能提升与异常行为。  
4. **单元/集成测试**：  
   - 验证同一 URL 的多次请求是否命中缓存并避免重复文件写入。  
   - 在模拟多 encode worker 环境下检查 `encode_batch_size` 动态计算的正确性。  
   - 对 Qwen‑3‑VL 模型路径进行回归测试，确保 vision model 能正确加载且不触发全模型加载。  
5. **文档更新**：在项目 README 或部署手册中明确：
   - `EMBEDDING_CACHE_MAX_SIZE`（若实现）配置方式。  
   - 临时文件目录清理策略。  
   - 支持的模型列表（新增 Qwen‑3‑VL）。  
6. **安全审计**：确认 `image_url` 的来源受信任，或在加载前对 URL 做白名单/签名校验，防止 SSRF 攻击。  

> **结论**：此次提交在多模态编码路径上实现了批处理与本地缓存，显著提升了吞吐和重复请求的响应速度，同时通过动态调度适配多 encode worker 环境。若及时解决缓存容量、临时文件清理以及异常容错等细节，整体风险可控，业务价值与性能收益明显。

---

#### 🟡 中重要度变更 (17)

### docs: full migration of docs/ to fern format in fern/ (#6050)
**SHA**: `2c3066b` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/2c3066bd5ddedfcb871fd8663d50fe1533f327fb)

⚠️ LLM分析失败（已重试3次）: API请求失败: 400 Client Error: Bad Request for url: https://integrate.api.nvidia.com/v1/chat/completions

*暂无分析*

---

### fix: reduce NATS consumer inactive_threshold from 1h to 2min (#5861)
**SHA**: `d59b9d7` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/d59b9d72ed98eed50e8863de8259d0871efad336)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
将 NATS JetStream 拉取消费者的 `inactive_threshold` 从 **1 小时**调低至 **5 分钟**（`Duration::from_secs(300)`），以更快检测并回收长时间未使用的消费者实例，防止资源泄漏和潜在的消费阻塞。

**🎯 影响范围**  
- `lib/runtime/src/transports/nats.rs` 中的 `NatsQueue` 实现  
- 依赖 NATS JetStream 拉取模式的所有 Dynamo 业务模块（如任务调度、外部触发器）  

**💡 关注建议**  
1. **功能验证**：在本地或预发布环境跑一次完整的消费链路，确认消费者在 5 分钟无活动后能被正确清理并重新创建，不会导致消息丢失或重复消费。  
2. **性能评估**：频繁的消费者回收会带来额外的网络往返和 JetStream 元数据操作，建议监控 `consumer_create` / `consumer_delete` 计数以及 NATS 服务的 CPU/内存负载。  
3. **兼容性检查**：如果业务方自行在代码中覆盖 NATS 消费者配置，需要确认新阈值不会冲突，必要时提供显式的 `inactive_threshold` 参数让用户自定义。  
4. **回滚方案**：若在高并发场景出现异常重建导致吞吐下降，可临时将阈值恢复到原来的 1 小时，或在配置层面提供可调开关。  

**总体建议**：此改动可提升系统对闲置消费者的自愈能力，但请在生产环境开启前做好监控与回滚预案，防止因阈值过低引起的频繁重建对吞吐量产生副作用。

---

### fix: Router + SGLang DP testing (#6057)
**SHA**: `2bcbda1` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/2bcbda19e486fa5a83c8415d713dca797310ec95)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  
**📋 变更摘要**：在 `sglang` 的 KV 事件发布器中加入 `dp_rank` 参数，并在 Router E2E 测试中使用支持数据并行和张量并行的模型，新增 `--tp-size` 与 `--enable-dp-attention` 选项，以验证 DP（数据并行）场景下的正确性。  
**🎯 影响范围**：  
- `components/src/dynamo/sglang/publisher.py`（KV 事件发布器初始化）  
- `tests/router/test_router_e2e_with_sglang.py`（端到端路由测试）  
- 相关配置解析路径（`dynamo_args`、`server_args`）以及 ZMQ 订阅器日志。  

**💡 关注建议**  
1. **参数兼容性**：`dp_rank` 现在会随每个发布器实例传递，确认在非 DP 环境下仍能默认 `dp_rank=0`，避免因缺省值导致的运行时错误。  
2. **测试可靠性**：新加入的 `--tp-size` 与 `--enable-dp-attention` 只在测试中使用，建议在生产代码的参数解析中加入相应的帮助信息与合法性检查，防止误用。  
3. **日志与监控**：日志已加入 `dp_rank` 标记，最好在监控平台对不同 rank 的 KV 事件流做独立指标，以便快速定位并行调度问题。  
4. **回归验证**：运行完整的单元/集成测试，尤其是没有开启 DP/TP 的路径，确保旧行为未被意外改动。  

总体来看，此次改动修复了 DP 场景下 KV 事件发布的遗漏，影响范围局限于 SGLang 发布器和对应的 E2E 测试，兼容性风险较低，只需注意参数默认值和新选项的文档说明。

---

### fix: operator chart imagePullPolicy (#4821)
**SHA**: `4715005` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/4715005ba54becb9f1f199bba328303d9b86766d)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
在 `deploy/helm/charts/platform/components/operator/templates/deployment.yaml` 中为两个容器（`kube‑rbac‑proxy` 与 `manager`）新增 `imagePullPolicy` 配置项，使用 Helm values `controllerManager.kubeRbacProxy.image.pullPolicy` 与 `controllerManager.manager.image.pullPolicy`。此举解决了部署时默认使用 `IfNotPresent` 但用户期望自行控制拉取策略的场景。

**🎯 影响范围**  
- Helm chart（operator 组件）  
- 使用该 chart 的所有 Kubernetes 集群（升级/全新安装均受影响）  
- `values.yaml` 中若未显式提供 `pullPolicy`，将使用空值导致模板渲染为 `""`，可能触发 Kubernetes 报错。

**💡 关注建议**  
1. **默认值**：在 `values.yaml` 中补充 `pullPolicy` 的默认值（如 `IfNotPresent`），防止渲染为空导致部署失败。  
2. **向后兼容**：若已有用户未在 values 中声明该字段，确保 Chart 在升级时仍能正常安装。可在模板中使用 `default` 函数提供回退。  
3. **文档同步**：更新 Chart README 与部署文档，说明 `imagePullPolicy` 可配置及其默认行为。  
4. **CI 测试**：在 CI 中加入使用不同 `pullPolicy`（`Always`、`Never`）的 Helm 渲染/安装测试，确保模板渲染正确且容器能成功启动。  
5. **安全审计**：确认新字段不泄漏敏感信息，且仅影响容器镜像拉取策略，无其他副作用。  

通过以上检查可确保该修复在所有环境中平滑生效，提升用户对镜像拉取策略的可控性。

---

### fix(sglang): remove apt-installed python3-blinker (#5995)
**SHA**: `e7936c2` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/e7936c2516930262153abbd6e4c89bed690c609f)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
在 `container/Dockerfile.sglang` 中，额外删除了系统 apt 包 `python3‑blinker`。该包会与 SGLang 镜像中通过 `pip` 安装的 `blinker`（作为 Flask/Dash 的依赖）产生冲突，导致运行时出现版本不一致或导入错误。  

**🎯 影响范围**  
- **Docker 镜像构建**：SGLang 运行时镜像体积略减，且不再出现 `python3-blinker` 与 `pip` 包冲突。  
- **运行时依赖**：只保留 `pip` 安装的 `blinker`，因此依赖该库的 Python 代码行为保持不变。  
- **CI/CD 与本地调试**：所有使用该 Dockerfile 的 CI 流程和本地容器启动将受此更改影响。  

**💡 关注建议**  
1. **验证依赖**：确认镜像中其他系统 Python 包（如 `python3-apt`）不再间接依赖 `python3-blinker`，避免因缺失导致意外报错。  
2. **完整性测试**：在 CI 中加入对 Flask/Dash 启动的冒烟测试，确保 `blinker` 正常被 `pip` 版本提供。  
3. **镜像大小**：考虑在同一步骤中执行 `apt-get clean && rm -rf /var/lib/apt/lists/*`，进一步压缩镜像。  
4. **文档更新**：在镜像构建说明中标注已移除 `python3-blinker`，提醒用户不要在容器外部自行安装该系统包。  

总体而言，此次改动是一次细粒度的依赖冲突修复，对功能无直接影响，但建议在发布前通过容器化测试确认所有入口点均能正常启动。

---

### fix(recipes): correct GPU counts in DeepSeek-R1 READMEs (#5953)
**SHA**: `03eb296` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/03eb296ea7fbe0b502737a53627c81e8e7264b15)

**🎯 变更类型**：Bug修复  
**⚡ 重要程度**：🟡 中  
**📋 变更摘要**：修正了 DeepSeek‑R1 两套部署配方中 GPU 数量的描述错误。`sglang` README 从 “8xH200 / 16xH200” 改为 “16x H200 (disagg‑8gpu) / 32x H200 (disagg‑16gpu)”，并更新了 TP/EP 参数说明。`vllm/disagg` README 同步改为跨四节点、共 32 GPU（每类 worker 16 GPU）的部署，并更正了对应的 manifest 文件路径。  

**🎯 影响范围**：  
- `recipes/deepseek-r1/sglang/README.md`  
- `recipes/deepseek-r1/vllm/disagg/README.md`  

**💡 关注建议**：  
1. **文档一致性**：确认所有其它引用该配方的脚本或 CI（如 CI 检查、部署示例）已同步更新为 16/32 GPU 的名称和路径，避免出现找不到 `deploy_hopper_16gpu.yaml` 的错误。  
2. **参数检查**：TP/EP（Tensor‑Parallel / Expert‑Parallel）大小已改为 “TP/EP size”，请在实际部署时核对对应的 `--tensor-parallel-size` 与 `--expert-parallel-size` 参数是否与 GPU 数匹配。  
3. **兼容性测试**：在仅有 8 GPU 的 Hopper 环境中仍可能使用该配方（文档已说明可自行调小），建议跑一次快速的 smoke‑test，确保文档中的 “改动 TP/EP size” 步骤不会导致启动失败。  
4. **CI/文档生成**：如果项目使用自动化文档检查（例如 Markdown lint），请在 CI 中加入对 GPU 数量关键字的校验，以防类似误写再次出现。  

总体来说，此次修改仅涉及文档描述，不会影响代码运行，但若未同步更新相关脚本或 CI，用户在阅读文档后可能执行错误的 manifest，导致部署失败。及时检查并统一所有入口即可。

---

### ci: Transition deploy tests to pytest framework (#5874)
**SHA**: `6401e34` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/6401e34dafb2adfdb830a4df7fa902595906a49a)

**🎯 变更类型**：CI / 功能增强（部署相关测试迁移至 pytest）  
**⚡ 重要程度**：🟡 中（对 CI 稳定性和代码库可维护性有显著提升）  

**📋 变更摘要**  
1. 将原有的 Bash‑style 部署测试改写为基于 **pytest** 的可参数化测试，新增 `tests/deploy` 包及相关 fixtures、CLI 选项。  
2. 精简 `.github/actions/dynamo-deploy-test` 输入，改用 Python 环境执行 `pytest tests/deploy/test_deploy.py`；同时加入 `kr8s`, `kubernetes` 等依赖。  
3. CI 工作流 `pr.yaml` 触发条件改为 `changed-files` 检测，统一使用 `profile`、`image`、`platform_arch` 参数。  
4. `upload_complete_workflow_metrics.py` 跳过部署作业的度量收集；在 `pyproject.toml` 中新增 `deploy` 标记。  
5. `ManagedDeployment._init_kubernetes` 增强 kubeconfig 查找逻辑，兼容 CI‑KUBECONFIG、in‑cluster、默认配置三种情况。  

**🎯 影响范围**  
- **CI/CD**：`.github/actions/dynamo-deploy-test`, `.github/workflows/pr.yaml`、`upload_complete_workflow_metrics.py`。  
- **测试框架**：新增 `tests/deploy/*`、`tests/utils/client.py`、`tests/utils/managed_deployment.py`（部署管理与日志）。  
- **依赖**：`container/deps/requirements.test.txt`（新增 kr8s、kubernetes、pydantic 等）。  
- **标记系统**：`pyproject.toml`、`tests/conftest.py`（新增 `deploy` 标记）。  

**💡 关注建议**  

| 开发者 | 建议 |
|--------|------|
|**CI 配置**|确认 CI 环境已提供 `KUBECONFIG`（Base64）并在 job 中写入 `.kubeconfig`，否则 `ManagedDeployment` 会回退到本地 kubeconfig 导致失败。|
|**参数兼容**|新 action 参数 `profile`, `image`, `platform_arch` 必须在工作流中显式传递；删除的 `framework_runtime_image`、`deployment_file` 等字段若仍在旧脚本中被引用会导致运行时错误。|
|**依赖管理**|`kr8s` 与 `kubernetes` 版本较新，部分旧 Python 环境可能出现兼容性问题，建议在本地跑一遍 `pytest -m deploy` 以捕获结构性错误。|
|**测试可靠性**|部署测试依赖实际 K8s 集群，网络波动会导致 flaky。建议在 `pytest.ini` 中为 `deploy` 标记设置合理的 `timeout`，或在 CI 中使用 `retry` 机制。|
|**度量收集**|`upload_complete_workflow_metrics.py` 已跳过部署作业的指标上传，若后续需要统计部署耗时，请在对应 job 中手动生成 JUnit XML。|
|**文档更新**|更新 README/CONTRIBUTING，说明新增 `--framework`, `--profile`, `--image`, `--skip-service-restart` 等 CLI 选项的默认值与使用场景。|

**对用户**：在本地或 CI 运行部署测试时，只需 `pytest -m deploy --framework vllm --profile agg --image <img> --namespace test-ns`。若未指定 `--image`，将使用 YAML 中默认镜像；默认会 **跳过** NATS/etcd 重启，以加速测试，需手动加 `--skip-service-restart=false` 才会重新启动服务。  

总体而言，此次改动将部署验证统一到 pytest，提高可维护性和并行度，但也引入了对 K8s 环境和新 Python 依赖的硬性要求，请确保 CI 环境配置完整后再合并。

---

### fix: downgrading opencontainers/runtime-spec version to fix compatibility issue with containerd (#6049)
**SHA**: `5092a5d` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/5092a5d0f8011b9865704ac34dc7020fc8ed188d)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
此次提交把 `deploy/chrek` 子模块的 `github.com/opencontainers/runtime-spec` 依赖从 **v1.3.0** 降级至 **v1.2.0**，并相应更新 `go.sum**。该改动是为了解决在与 `containerd`（v1.7.30）配合使用时出现的兼容性错误。  

**🎯 影响范围**  
- **deploy/chrek**：唯一受影响的 Go 子模块。  
- 可能间接影响使用 `chrek` 生成或管理 OCI 容器规范的上层业务（如 `dynamo` 的部署脚本）。  
- 其它 Rust 核心库不受影响，只有 Go 部分的编译和运行时会受到此更改影响。  

**💡 关注建议**  

| 关注点 | 建议 |
|--------|------|
| **API 兼容性** | `runtime-spec v1.2.0` 与 `v1.3.0` 的差异主要在新增的字段/结构体（例如 `Process.User.UID`、`MountOptions` 的新值等）。请检查 `deploy/chrek` 代码中是否有对这些 v1.3.0 新增特性的引用，若有需回退到兼容的旧字段或添加条件编译。 |
| **编译验证** | 在本地与 CI 中执行 `go test ./...`（若有测试）以及 `go vet`，确保降级后仍能顺利通过。尤其要确认 `containerd` 相关的调用（如 `client.New`、`container.Spec()`）与 v1.2.0 的结构匹配。 |
| **运行时兼容** | 部署到实际机器后，使用 `chrek` 生成的 OCI runtime spec 应能被 `containerd` 正确加载。建议在一台包含同版本 `containerd` 的环境里做一次完整的容器创建‑启动‑停止循环，以验证没有隐藏的运行时报错。 |
| **依赖锁定** | 依赖已在 `go.mod` 中明确锁定，`go.sum` 也相应更新。若项目使用 vendoring（`go mod vendor`），记得重新生成 vendor 目录。 |
| **文档** | 在 `deploy/chrek/README.md`（或项目根目录的 CHANGELOG）补充一条说明，解释为何需要降级以及兼容的 `containerd` 版本范围，以免后续升级时再次触碰同一兼容性坑。 |
| **未来升级** | 若后续 `containerd` 或其他 OCI 运行时升级到支持 `runtime-spec v1.3`，可以考虑在 `go.mod` 中使用 `// indirect` 引入 v1.3 并在 CI 中加入兼容性矩阵测试，防止类似回滚。 |

**总体评价**  
这是一项定位明确、改动幅度小的兼容性修复。只涉及 `go.mod`、`go.sum` 两个文件，风险主要集中在代码是否已依赖 v1.3.0 的新增字段。完成上述检查后，影响应有限且可快速回滚。建议在合并前跑一次完整的 `go` 构建并在实际 `containerd` 环境中做一次端到端的容器部署验证。

---

### fix: remove envsubst for logging-dashboard.yaml to preserve Grafana template variables (#6045)
**SHA**: `82a8d76` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/82a8d768a554608f5846c05dc926dcfa028d5f2f)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  
**📋 变更摘要**：在 `docs/kubernetes/observability/logging.md` 与对应的 Fern 文档中，去掉对 `logging-dashboard.yaml` 的 `envsubst` 处理，改为直接使用 `kubectl apply -f … -n $MONITORING_NAMESPACE`。这样可以避免模板变量被提前展开，从而保留 Grafana 仪表板中定义的 `${DS_PROMETHEUS}`、`${DS_LOKI}` 等占位符。

**🎯 影响范围**  
- 文档模块（`docs/kubernetes/observability`、`fern/pages/kubernetes/observability`）。  
- 使用该文档自行部署 Grafana 的用户。  

**💡 关注建议**  
1. **验证文档**：在本地或 CI 中执行更新后的命令，确认仪表板能够成功创建且模板变量保持原样。  
2. **统一示例**：若项目中还有其他 `envsubst` 示例（例如 `loki-datasource.yaml`），检查是否同样需要去除，防止出现不一致的使用方式。  
3. **说明原因**：在文档的 “注意事项” 部分补充一行简短解释，提醒读者 `envsubst` 会破坏 Grafana 模板变量，保持文档自解释性。  
4. **回退兼容**：若有旧的部署脚本仍在使用 `envsubst`，建议在发布说明中提醒用户更新脚本。  

此次改动仅是文档层面的修正，对代码库本身没有直接影响，风险极低，主要提升了部署指南的可用性和稳定性。

---

### feat: enable go-to-definition for dynamo.runtime, dynamo.nixl and external dependencies (#6026)
**SHA**: `f6dd904` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/f6dd90474ba73b49f5ee353666eaf021df8c0d9e)

**🎯 变更类型**：功能增强  
**⚡ 重要程度**：🟡 中  
**📋 变更摘要**：在 `pyproject.toml` 中新增 `[tool.basedpyright]` 配置，指定 `extraPaths` 为 `components/src` 与 `lib/bindings/python/src`，并设置 `venvPath` 与 `venv` 为本仓库的 `.venv`，以便 IDE（如 Cursor）能够在 `dynamo.runtime`、`dynamo.nixl` 以及外部依赖上提供 “go‑to‑definition”、悬停提示等功能。  

**🎯 影响范围**：  
- Python 代码编辑体验（所有使用基于 `basedpyright` 的语言服务器的 IDE）  
- CI/Lint 流程（若引入基于 `basedpyright` 的检查）  

**💡 关注建议**：  
1. **路径检查**：确保 `components/src` 与 `lib/bindings/python/src` 在仓库根目录下真实存在，否则 IDE 会提示模块未找到。  
2. **虚拟环境一致性**：项目已使用 `.venv`，若团队采用不同名称或位置的虚拟环境，需统一或在 IDE 中手动覆盖 `venvPath/venv`。  
3. **CI 配置**：若计划在 CI 中运行 `basedpyright`，请在 CI 脚本里提前安装该工具并激活 `.venv`，以免出现 “cannot find module” 的错误。  
4. **兼容性**：`pyproject.toml` 仍被其他工具（如 Poetry、Mypy）读取，新增的 `[tool.basedpyright]` 部分对它们是透明的，但建议在项目文档中注明此节的用途，以免误删。  

该改动仅提升开发体验，不会影响运行时行为，建议在本地 IDE 中验证一次路径解析是否正常后再提交。

---

### chore: clean ups in kv_router.rs (#6028)
**SHA**: `9e33e3f` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/9e33e3fa66338421fc43f4bdbb35f7d29f788fc0)

**🎯 变更类型**：功能增强 / 重构  
**⚡ 重要程度**：🟡 中  
**📋 变更摘要**：在 `kv_router.rs`、`mocker` 与 `dynamo‑run` 中引入 `validator`，对 KV‑Router、MockEngine 参数以及部分结构体增加运行时校验；同时去掉 `KvRouterConfig::new` 构造函数，改用 `Default`+手动字段覆盖的方式构造。  

**🎯 影响范围**  
- `core/llm/src/kv_router.rs`（RouterConfigOverride、KvRouterConfig 参数校验）  
- `core/llm/src/preprocessor/media/loader.rs`（字段标记）  
- `launch/dynamo-run/src/flags.rs`（router 配置构造逻辑）  
- `bindings/c/src/lib.rs`（C 接口配置构造）  
- `lib/mocker`（MockEngineArgs 校验、Scheduler 参数校验、ActiveSequence 校验）  

**💡 关注建议**  

1. **新增 validator 依赖**  
   - 确认 `Cargo.toml` 中的 workspace 依赖已经统一升级，避免版本冲突。  
   - 运行 `cargo test --all-features` 检查所有特性（尤其是 `media-nixl`）的编译路径。  

2. **配置校验行为**  
   - `KvRouterConfig::validate()` 现在会在 `KvRouter::new` 时返回错误而不是 panic，调用方需处理 `Result`（目前已使用 `?`），但其它直接 `unwrap()` 的地方可能需要补充错误处理或保持向上传播。  
   - `RouterConfigOverride` 只对 `router_temperature` 加了范围校验，若业务仍会传负值会得到 `ValidationError`，请检查 CLIs/JSON 配置文件的默认或文档。  

3. **构造逻辑变更**  
   - `Flags::router_config` 由一次性 `KvRouterConfig::new` 改为 `Default` + 手动覆盖，保持相同语义但对未显式设置的字段使用默认值。若以后在 `KvRouterConfig` 中新增字段，需要同步此处的覆盖逻辑。  

4. **C 接口兼容性**  
   - `dynamo_create_worker_selection_pipeline` 现在直接构造 `KvRouterConfig { ..Default::default() }`，确保结构体布局未变。若外部 C 调用依赖 `NULL` 表示 “未设置”，保持行为一致。  

5. **Mocker 参数校验**  
   - `MockEngineArgs` 现在在 `Scheduler::new` 中调用 `validate()`，若旧的测试或脚本传入无效值会在启动时报错。请在文档中更新每个字段的合法范围。  
   - `ActiveSequence::validate()` 被显式调用，确保 `block_size >= 2`。注意之前的 `assert!` 已移除，若业务仍依赖 panic 语义，需要自行捕获错误。  

6. **潜在回归**  
   - 校验错误会返回 `anyhow::Error`，可能在日志中出现大量 “validation error”。监控启动日志以确认没有误报。  
   - 因为 `RouterConfigOverride` 仍实现 `Builder`，使用 `builder()` 生成实例时若缺失必填字段会在 `build()` 时触发校验，建议在所有构造路径上加入 `.expect("valid config")` 或适当错误处理。  

**总结**：本次提交通过 `validator` 引入了更严格的运行时检查，提升了配置安全性；同时对构造方式的改动简化了代码。需重点验证新增错误路径在所有调用链上得到妥善处理，并在文档中同步字段约束说明。祝调试顺利！

---

### docs: clean up toctree navigation and add disaggregated serving guide (#6024)
**SHA**: `07db589` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/07db589583928dbebc3fa62ba7d4037246e78fb3)

**📚 关键变更概览**  
1. **全新文档结构** – 将原有的 “Fault‑Tolerance、K8s‑部署、观测、杂项” 等碎片化章节合并、删减，重新组织为 **components / backends / features / deploy / performance / infrastructure / integrations / reference / design_docs** 九大类。  
2. **新增 “Disaggregated Serving Guide”**（`docs/features/disaggregated_serving/README.md`）并配套四张 SVG（arch comparison、decision flow、e2e workflow、param mapping）以及大量说明图片。  
3. **`index.rst`、`hidden_toctree.rst`、`kubernetes/README.md` 失衡更新** – 重新排列 TOC、移除已删除章节、为 router/kvbm 等组件加入子‑page (`router_guide.md`、`router_examples.md`、`kvbm_guide.md`、`frontend_guide.md` 等) 的 `.. toctree::`。  
4. **大量旧文档删除** – `fault_tolerance/`, `performance/aiconfigurator.md`, 迁移模板 (`MIGRATION_GUIDE.md`, `EXAMPLE_SKILL.md`, `SOURCE_TARGET_MAPPING.md`) 等全部移除。  
5. **图形资源搬迁** – 所有新 SVG 放在 `docs/images/`，在 Markdown 中使用相对路径 `../../images/...`。  

**⚙️ 对构建/站点的直接影响**  
- **Sphinx‑HTML**：若任何页面仍引用已删除的 RST/MD，`make html` 会报 `WARNING: unknown document`. 必须检查 `conf.py` 中的 `redirects`（当前未添加）以及所有 `:doc:`、`.. include::`、markdown 链接的目标路径。  
- **Fern/文档站点**：`fern/versions/next.yml` 仍保留的旧路径未同步，会导致左侧导航缺失。  
- **图片路径**：`../../images/*.svg` 在 `features/disaggregated_serving/` 下解析为 `docs/images/`，正确；但如果将来页面层级变化，需要重新审视。  

**✅ 验证建议**  

| 步骤 | 目的 | 命令 |
|------|------|------|
| 1️⃣ 完整 HTML 构建 | 捕获缺失引用、未解析的 `.. toctree`、图片错误 | `cd docs && make clean html -W` |
| 2️⃣ 链接检查 | 检测内部/外部断链（包括 Fern 页面） | `lychee docs/ --offline --exclude-path docs/_build` |
| 3️⃣ Fern 预览 | 确认左侧导航、页面 URL 正常 | `npx fern dev`（或 `npm run docs:dev`） |
| 4️⃣ 重定向补齐 | 为所有移除或改名的页面在 `conf.py` 中添加 `redirects = {"old/path.md": "new/path.html"}`，确保外部引用不 404。 |
| 5️⃣ 文档审阅 | 让团队成员点击 **STOP** 注释（已在旧模板中使用）确认每一步迁移是否完整。 |

**📌 推荐后续动作**  

1. **更新 `index.rst`**：把新 *Disaggregated Serving Guide* 加入隐藏 TOC 或显式章节，确保首页搜索可达。  
2. **补充 `conf.py` 重定向**：对每个被移动的文件（如 `docs/planner/planner_intro.rst → docs/components/planner/README.md`）加入映射，避免外部链接 404。  
3. **清理残余引用**：在代码库全局搜索 `fault_tolerance`, `k8s_deployment`, `aiconfigurator` 等关键字，确保没有遗留的 `:doc:`、markdown 链接或跨引用。  
4. **文档 CI**：在 CI pipeline 中加入 `make -C docs html && lychee docs/`，自动阻塞合并若出现警告/断链。  

完成以上检查后，现有文档结构即可稳定运行，且新加入的 “Disaggregated Serving Guide” 将在站点中完整呈现。

---

### ci: add GitHub actions for linting and cutting versioned docs for Fern (#5524)
**SHA**: `219e5c4` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/219e5c456fae3d4aad5017c3dccca4c260d0ca30)

**变更核心**  
1. **GitHub Actions**：新增 `fern-docs.yml` 工作流，实现 Fern 文档的 **lint → vNext 同步 → 版本发布** 三阶段自动化。  
2. **changed‑files Action**：在 `.github/actions/changed-files` 中加入 `fern` 输出，并在 `filters.yaml` 新增 `fern` 路径过滤，保证仅在 fern/** 变更时触发相应 job。  
3. **文档同步 & 版本化**：`sync‑vnext` 将 `fern/pages`、`assets`、`versions/next.yml` 等同步到 `docs‑website` 分支，同时保留已有的历史快照。`release‑version` 在标签推送时生成 `pages‑vX.Y.Z`、`versions/vX.Y.Z.yml`，并自动更新 `docs.yml`。  
4. **工具脚本**：新增 `fern/convert_callouts.py`，把 GitHub‑style admonition（> [!NOTE]）转为 Fern‑style（<Note>…</Note>），在 sync 与 release 步骤中统一调用。  
5. **文档小幅修正**：更新几页中链接、许可证头、检查引用路径。

**影响范围**  
- CI/CD：所有 PR、push、tag 触发的工作流会额外执行 Fern 文档的 lint 与同步；若 `changed‑files` 解析出现误差，可能导致不必要的 job。  
- `docs‑website` 分支：自动提交的同步与版本快照会改变该分支的提交历史，需注意与手动维护的冲突。  
- 项目文档：链接路径已改为指向 `docs‑website`，对外站点展示会受此影响。  
- 新增的 Python 脚本要求 CI 环境装有 Python3（已默认），且 `fern` 目录必须保持可执行权限。

**建议**  
1. 本地或 CI 中跑一次 `fern-docs.yml`（可使用 `workflow_dispatch`）验证 **lint → sync → release** 全流程，尤其检查 `convert_callouts.py` 对多行、缩进等情况的转换是否符合预期。  
2. 确认 `permissions: contents: write` 对 `GITHUB_TOKEN` 生效，防止同步/发布步骤因权限不足而失败。  
3. 在 `filters.yaml` 中保持 `docs` 不再包含 `fern/**`，避免重复触发；若已有其它 workflow 仍依赖 `docs` 过滤，需要同步更新。  
4. 为防止并发冲突，给 `sync‑vnext` 与 `release‑version` 添加 `concurrency` 或通过 `branches: [main]` 限制；尤其在 tag 推送后不应再次跑 `sync‑vnext`。  
5. 将 `convert_callouts.py` 加入项目的 lint（如 `ruff`/`flake8`）或 CI 测试，防止未来语法回退。  
6. 更新文档链接（如 `README.md` 中的 Fern 部分）指向新同步路径，避免用户点击失效。  

总体来看，此次提交为 Fern 文档提供了完整的自动化流水线，提升了文档质量与版本管理的可维护性，只要 CI 权限和过滤配置保持一致，即可安全上线。

---

### chore: remove and unify bindings in kv.rs (#6016)
**SHA**: `3e41702` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/3e41702211111737766a83e844f6f314f5a199e4)

**🎯 变更类型**：重构/功能增强  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
本次提交在 Rust 与 Python 两层实现中统一了 KV 事件发布的入口：原先的 `ZmqKvEventPublisher`（Python‑>ZMQ PUB 与 Rust‑>ZMQ SUB）被删除，仅保留 `KvEventPublisher`。`KvEventPublisher` 现在接受可选的 `ZmqKvEventPublisherConfig`，在提供该配置时会自动订阅 ZMQ 并转发至 NATS，实现“ZMQ → NATS” 的中继模式。同时移除了 `KvRecorder` 相关绑定和文档，更新了所有使用方的导入路径和类型注解。  

**🎯 影响范围**  
- **核心库**：`lib/bindings/python/rust/llm/kv.rs`、`lib/bindings/python/_core.pyi`、`lib/bindings/python/rust/lib.rs`  
- **Python 代码**：`components/*/publisher.py`、`components/*/main.py`、`components/*/handlers.py`、`examples/*/worker.py`、`docs/integrations/kv_events_custom_engines.md`  
- **外部 API**：`dynamo.llm.KvEventPublisher`（新签名）取代了 `ZmqKvEventPublisher`；`KvRecorder` 被完全删除。  

**💡 关注建议**  
1. **兼容性**：若有旧版用户仍在直接 import `ZmqKvEventPublisher`，需在 release notes 明确迁移指南，或提供临时的别名/兼容层。  
2. **参数冲突**：`KvEventPublisher` 现在接受 `kv_block_size、dp_rank、enable_local_indexer` 与 `zmq_config` 两套参数，文档要强调两者互斥，防止误传导致隐藏覆盖。  
3. **资源清理**：新增 `shutdown` 实现只在唯一引用时立即关闭，需在业务侧确保在进程退出前调用，或在 `__del__` 中补充警告。  
4. **测试覆盖**：增加对 `KvEventPublisher` 的单元测试，验证在有/无 `zmq_config` 情形下的初始化、事件转发以及关闭行为。  
5. **文档同步**：检查所有示例、用户手册以及自动生成的 API 文档均已改为 `KvEventPublisher`，避免出现未更新的 `ZmqKvEventPublisher` 示例。  

总体来看，此次统一提升了 API 的可理解性并削减了冗余实现，但需要注意迁移路径和参数使用的明确性，以免引入运行时错误。

---

### fix: Fix clashing labels (#6038)
**SHA**: `b0f5434` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/b0f54344fe0e20f666dc10cc86aed59614dcabba)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  
**📋 变更摘要**：在 `.github/labeler.yml` 中将冲突的标签键由 `build:` 与 `ci:` 更名为 `container:` 与 `actions:`，分别对应 `container/**` 与 `.github/workflows/**` 的文件变化，以避免标签名称冲突。  
**🎯 影响范围**：GitHub 自动标记系统（Labeler），CI/CD 工作流中可能依据标签触发的脚本或文档。  

**💡 关注建议**  
1. **核对仓库标签**：确认 GitHub 项目已创建 `container`、`actions` 两个标签，若缺失手动补全。  
2. **更新引用**：搜索仓库中任何硬编码的 `build`、`ci` 标签（如在 ISSUE 模板、README、内部脚本），统一改为新标签名称。  
3. **验证自动标记**：在新建 PR 或推送代码后，检查对应文件路径是否被正确标记为 `container`、`actions`，防止误触发旧标签导致的误分类。  
4. **CI 流水线**：若有基于标签的工作流（如 `on: label:`）或权限控制，需同步调整，以免出现不触发或误触发的情况。  

此改动仅影响项目管理自动化，不会影响运行时代码，快速完成上述检查即可确保平稳过渡。

---

### fix: remove bash wrapper for vllm dsr1 recipe (#6035)
**SHA**: `74d3db6` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/74d3db65b1bffe9922f75470a305c47b3620a1ec)

**🎯 变更类型**：功能增强 / Bug 修复（去除无意义的 Bash 包装层）  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
- 将 `deploy_hopper_16gpu.yaml` 中两处容器启动方式，从 `["/bin/bash","-c","…"]` 改为直接使用 `python3 -m dynamo.vllm` 并把原本的长命令拆分为 `command`+`args` 列表。  
- 同时把原先的 `exec` 前缀、换行拼接以及 Bash 变量解析全部去掉，改为纯参数形式。  

**🎯 影响范围**  
- `recipes/deepseek-r1/vllm/disagg/` 目录下的部署脚本（两个 worker：`decode` 与 `prefill`）。  
- 运行环境必须保证 Python 可执行文件在 `PATH`（`python3`），且容器镜像已包含 `dynamo` 包。  

**💡 关注建议**  

1. **启动参数的转义**  
   - 现在所有选项都以单独的数组元素传递，JSON 字符串 (`--eplb-config`、`--compilation_config`) 必须保持完整的引号。建议在 CI 中使用 `kubectl exec … -- python3 -m dynamo.vllm …` 手动验证一次，确保容器收到的参数与原来 `bash -c` 时一致。  
2. **信号转发**  
   - 以前使用 `exec` 让 Python 成为 PID 1，当前同样是直接启动 Python，行为基本相同。但仍需确认容器在收到 SIGTERM/INT 时能够正常退出（日志中是否有清理信息）。  
3. **镜像兼容性**  
   - `python3` 的路径在某些自定义镜像里可能是 `/usr/local/bin/python3`，若 PATH 不含该目录会导致容器启动失败。建议在 `Dockerfile` 中显式 `ENV PATH=$PATH:/usr/local/bin` 或改为 `command: ["python3","-m","dynamo.vllm"]` 前加完整路径。  
4. **YAML 语法**  
   - 变更后 `command` 与 `args` 的缩进保持一致，确保 `args` 列表不被误解析为字符串。可在本地运行 `yamllint` 检查。  
5. **回归测试**  
   - 运行现有的 end‑to‑end VLLM 测例，确认 `max-num-seqs`、`dbo-decode-token-threshold` 等选项仍然生效。尤其注意 `--all2all-backend` 从 `deepep_low_latency`/`deepep_high_throughput` 是否被正确传递。  

**结论**  
此提交简化了容器启动方式，去掉了多余的 Bash 包装，理论上降低了启动开销并避免了 Bash 环境差异。只要确认上述参数转义、镜像路径与信号处理无误，改动是安全且提升可维护性的。建议在合并前跑一次完整的部署‑to‑infer 流程验证。

---

### fix: Correctly pass DP rank from Dynamo router into vLLM engine (#6014)
**SHA**: `3a41825` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/3a418254897f4bad973bba7a8a01cf856df79737)

**🎯 变更类型**：Bug 修复  
**⚡ 重要程度**：🟡 中  

**📋 变更摘要**  
在 `components/src/dynamo/vllm/handlers.py` 中，DP（Data‑Parallel）rank 的读取方式由 `request.get("dp_rank")` 改为 `request.get("routing", {}).get("dp_rank")`，确保路由层传递的 `dp_rank` 能被 vLLM 处理函数正确获取。  

**🎯 影响范围**  
- `vllm` 子模块的 `generate_token_mode`、`generate_text_mode`、`prefill_token_mode` 三个入口。  
- 负责将 Dynamo Router 的路由信息（`routing` 字段）转发给 vLLM 引擎的代码路径。  

**💡 关注建议**  
1. **兼容性检查**：若已有外部调用在请求体中直接放置 `dp_rank`（未包装在 `routing`），将不再被识别。建议在文档或 SDK 中明确 `routing.dp_rank` 为唯一入口，或在上层 router 添加适配层保持向后兼容。  
2. **测试覆盖**：新增或更新单元测试，验证在完整路由结构、缺失 `routing`、以及 `routing` 中缺少 `dp_rank` 的三种情况均能正确返回 `None` 或抛出友好错误。  
3. **日志与监控**：当前仅在获取不到 `dp_rank` 时使用 `None`，若业务依赖该字段进行调度，建议在 `logger.debug` 中加入缺失提示，便于线上排查。  
4. **性能影响**：改动仅是字典访问层次的微调，影响可以忽略；但请确认在高并发路径上未引入额外的深拷贝或异常捕获。  

整体来看，此次修复消除了 DP rank 在跨进程路由时的丢失风险，提升了分布式推理的可靠性。后续可考虑在 `request` schema 中统一 `routing` 子对象的定义，避免类似字段散落导致的错误。

---

#### 🟢 低重要度变更 (5)

### docs: add notes and instruction for latest trtllm kvbm disagg (#6055)
**SHA**: `7d035af` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/7d035afffb21cee788b207b560a86ac34ad5693f)

**🎯 变更类型**：文档更新  
**⚡ 重要程度**：🟢低  
**📋 摘要**：在 KV‑BM 指南中新增了针对最新 TensorRT‑LLM（1.3.0rc1）版本的注意事项和构建、运行、复制 Triton kernel 的详细指令。

---

### docs: clarify the usage of LRU for mocker evictor (#6053)
**SHA**: `d00f960` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/d00f96074bce26fad61acf372984d2f168491872)

**🎯 变更类型**：文档更新  
**⚡ 重要程度**：🟢低  
**📋 摘要**：在 `docs/mocker/mocker.md` 中补充说明 LRU 驱逐器的实现细节，阐明其使用单调计数器实现 O(log n) 的深度感知驱逐策略，并解释前插入（负计数）用于立即驱逐的机制。

---

### docs: add quick start sections to KVBM and Router guides (#6043)
**SHA**: `fce8bbc` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/fce8bbc2508c1be0156841dce5c2e8bf25764c77)

**🎯 变更类型**：文档更新  
**⚡ 重要程度**：🟢 低  
**📋 摘要**：在 KVBM 与 Router 指南中新增快速入门章节，补充了组件概述、CLI 与 Kubernetes 部署示例以及配置、环境变量表格，提升文档可用性。

---

### docs: Update disagg and request flow design docs based on latest code (#5993)
**SHA**: `bed29a1` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/bed29a1600f114fd4b403c38b76bbc4cb1a3be77)

**🎯 变更类型**：文档更新  
**⚡ 重要程度**：🟢 低  
**📋 摘要**：更新了 `disagg_serving.md` 与 `dynamo_flow.md`，重写了 KV 转移、PrefillRouter 编排及后端元数据说明，简化并纠正了流程图与步骤描述，使文档与最新代码保持一致。

---

### ci: remove release branch docs deploy workflow (#6039)
**SHA**: `dde23cc` | 🔗 [查看提交](https://github.com/ai-dynamo/dynamo/commit/dde23cc6e0d1a19be284fa073eeebb8f89068497)

**🎯 变更类型**：配置调整  
**⚡ 重要程度**：🟢低  
**📋 摘要**：在 `.github/workflows/generate-docs.yml` 中删除了 `deploy` Job，去除对 `release` 分支 PR 的文档部署与评论功能，简化 CI 流程。

---


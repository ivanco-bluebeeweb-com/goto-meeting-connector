# GoTo Meeting Connector — Discovery & Feature Matrix

## 1. Classification of Capabilities

| Capability | Inbound (Imperal -> GoTo Meeting) | Outbound (GoTo Meeting -> Imperal) | Coverage |
| :--- | :---: | :---: | :---: |
| Core Video/Comm Operations | Write (Create/Delete) | Read (List/Get) | Both |
| Credentials & Connectivity | Write (Connect/Disconnect) | Read (List Connections) | Both |
| Health & Availability Audit | Analytical (Inspect status & resources) | - | Internal |

---

## 2. Feature Tiers
- **Tier 1 (Core)**: Meetings CRUD, historical & scheduled meeting listing, account health audit
- **Tier 2 (Audit & Analytics)**: Автоматическая проверка прав и доступности ресурсов.

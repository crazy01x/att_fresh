# atualizacoes_fresh

Repositório-base para centralizar atualizações do app Fresh e do runtime/linguagem.

## Estrutura

- `updates/app/manifest.json`: versão e artefato do app
- `updates/runtime/manifest.json`: versão e artefato do runtime/linguagem
- `scripts/validate-manifests.sh`: valida os manifests localmente e no CI
- `.github/workflows/ci.yml`: valida PRs e pushes
- `.github/workflows/release-manifests.yml`: publica release manual dos manifests

## Como atualizar

1. Edite o manifest necessário (`app` e/ou `runtime`).
2. Atualize versão, checksum SHA-256, URL de download, data de publicação e notas.
3. Rode:

```bash
./scripts/validate-manifests.sh
```

4. Abra PR seguindo o template.

## Objetivo para automação por IA

Este repositório foi preparado para que agentes (IA) consigam:

- aplicar atualizações de forma previsível (via manifest);
- validar automaticamente no CI;
- submeter PR com checklist de revisão completo.

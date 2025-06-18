# Sugestões de Gradientes Alternativos para Melhor Legibilidade

## 🎨 Opções de Gradientes Claros

### Opção 1: Tons de Azul Suave

```css
background: linear-gradient(
  135deg,
  #e3f2fd 0%,
  #ffffff 100%
); /* Azul muito claro */
background: linear-gradient(
  135deg,
  #f8f9fa 0%,
  #e8f4fd 100%
); /* Cinza + azul claro */
```

### Opção 2: Tons de Verde Suave

```css
background: linear-gradient(
  135deg,
  #f1f8e9 0%,
  #ffffff 100%
); /* Verde muito claro */
background: linear-gradient(
  135deg,
  #f8f9fa 0%,
  #e8f5e8 100%
); /* Cinza + verde claro */
```

### Opção 3: Gradientes Neutros (Recomendado)

```css
background: linear-gradient(
  135deg,
  #ffffff 0%,
  #f8f9fa 100%
); /* Branco para cinza claro */
background: linear-gradient(
  135deg,
  #fafbfc 0%,
  #e9ecef 100%
); /* Cinza ultra claro */
```

### Opção 4: Tons Quentes Suaves

```css
background: linear-gradient(
  135deg,
  #fff9e6 0%,
  #ffffff 100%
); /* Amarelo muito claro */
background: linear-gradient(
  135deg,
  #fdf6f0 0%,
  #ffffff 100%
); /* Laranja muito claro */
```

## ✅ Regras de Contraste para Legibilidade

1. **Proporção de contraste mínima**: 4.5:1 para texto normal
2. **Texto escuro em fundo claro**: `#212529` ou `#495057`
3. **Evitar cores muito saturadas** em grandes áreas
4. **Testar com diferentes dispositivos** e configurações

## 🔧 Implementação Atual (Corrigida)

```css
/* Backgrounds claros com texto escuro */
.file-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  color: #212529; /* Texto escuro para boa legibilidade */
}

.step-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #212529;
}

.upload-area {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  color: #495057;
}
```

## 🎯 Alternativas Sem Gradiente

Se preferir evitar gradientes completamente:

```css
/* Opção sólida simples */
.file-card {
  background: #ffffff;
  border: 1px solid #dee2e6;
}

/* Opção com sombra sutil */
.step-header {
  background: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
```

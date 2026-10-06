# Portfolio-Fotografico
Portfólio de Fotográfia, desenvolvido com foco na experiência do usuário, projetos do artista e na apresentação visual das fotografias.


Descrição do Projeto
Este projeto é um site portfólio para fotógrafos. O design minimalista coloca as fotografias em destaque, com uma navegação intuitiva e layout responsivo que se adapta a diferentes dispositivos.

**O portfólio apresenta:**

Layout moderno que valoriza as imagens

Navegação lateral fixa com informações de contato

Grid responsivo para galeria de fotos

Animações para melhor experiência do usuário

Design totalmente responsivo para mobile e desktop

**Recursos e Funcionalidades:**

Design Responsivo: Adapta-se perfeitamente a dispositivos móveis, tablets e desktops

Navegação Intuitiva: Menu lateral de fácil acesso

Galeria de Imagens: Layout em grid com efeitos hover para informações

Animações Suaves: Transições e efeitos visuais que melhoram a experiência

Integração com Redes Sociais: Links para Instagram, Twitter e outras plataformas



**Tecnologias Utilizadas**

HTML5: Estrutura semântica do projeto

CSS3: Estilização com Flexbox, Grid e variáveis CSS

JavaScript: Interatividade e funcionalidades dinâmicas

Font Awesome: Ícones para redes sociais

**Otimização das fotografias**

As páginas usam versões WebP responsivas em `fotos/optimized/`, com larguras de
até 480, 960, 1600 e 2400 pixels. O navegador escolhe a versão adequada à tela.
As primeiras imagens têm prioridade de carregamento; as demais usam o
carregamento nativo sob demanda (`loading="lazy"`). A galeria só carrega a
versão ampliada quando a foto é aberta. Os originais em `fotos/` são preservados.

Para gerar as versões de novas fotos no macOS, instale o conversor com
`brew install webp` e execute `python3 scripts/optimize-images.py`. O script
atualiza `fotos/optimized/manifest.json` com os caminhos e as dimensões; use essas
informações nos atributos `src`, `srcset`, `sizes`, `width` e `height` do HTML.
Na galeria, configure também `data-full-src` com a maior versão para o modal.

Ao publicar, envie os arquivos HTML e a pasta `fotos/optimized/` juntos.


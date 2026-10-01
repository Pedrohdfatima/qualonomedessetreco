CATÁLOGO DIGITAL INTELIGENTE DE CORTES
App único em Python (tkinter), todas as telas conectadas na mesma
janela, com cadastro/login salvos em arquivo (sem banco de dados por
enquanto).

COMO RODAR
----------
Único ponto de entrada: main.py
Mantenha todos os arquivos na MESMA pasta e rode:

    python3 main.py

FLUXO DO APP
------------
1. Abre direto na tela de Login. Pressionar Enter nos campos também
   envia o formulário (não precisa clicar em "Entrar").
2. Sem conta? Clique em "Cadastre-se" (não tem mais abas/tabs nessa
   tela, é só o formulário). Enter nos campos também envia.
3. Ao cadastrar, os dados são gravados em LOGINS/<usuario>.txt — a
   pasta LOGINS/ é criada automaticamente nesse momento (não existe
   antes do primeiro cadastro).
4. O cadastro NÃO loga automaticamente: você volta para o Login com o
   usuário pré-preenchido, e precisa confirmar a senha para entrar.
5. Login válido -> vai para o Dashboard.
6. Barra lateral: Início, Catálogo, Recomendações, Informações do
   usuário, Sair. (Não existe mais "Favoritos".)
7. Catálogo: a busca filtra os cortes em tempo real conforme você
   digita (compara com o nome e a categoria de cada corte).
8. Recomendações: agora tem o questionário (tipo de cabelo, formato
   do rosto, estilo, manutenção) que antes ficava em "Perfil". Depois
   de clicar em "Ver recomendações", aparece a lista de cortes
   sugeridos, com opção de "Refazer questionário".
9. Informações do usuário: mostra nome, usuário e e-mail de quem está
   logado (dados vindos do cadastro).

ARQUIVOS
--------
main.py                    -> ponto de entrada único (rode este)
theme.py                   -> paleta de cores
components.py              -> sidebar navegável, cartões, cabeçalhos
storage.py                 -> salva/lê usuários em LOGINS/*.txt

login_frame.py              -> Tela 1: Login (Enter funciona)
cadastro_frame.py           -> Tela 2: Cadastro (sem abas, Enter funciona)
dashboard_frame.py          -> Tela 3: Dashboard
catalogo_frame.py           -> Tela 4: Catálogo (busca funcional)
detalhe_frame.py            -> Tela 5: Detalhes do Corte
informacoes_frame.py        -> Tela 6: Informações do usuário (era "Perfil")
recomendacoes_frame.py      -> Tela 7: Recomendações (agora com o questionário)
admin_frame.py              -> Tela 8: Administrativa

LOGINS/                     -> criada automaticamente após o 1º cadastro

REQUISITOS
----------
Apenas Python 3 com tkinter (biblioteca padrão). No Linux, se faltar:
sudo apt install python3-tk

OBSERVAÇÃO DE SEGURANÇA
------------------------
As senhas são gravadas com hash simples (sha256), só para não ficarem
em texto puro no arquivo — não é um esquema de produção, é um cuidado
básico enquanto não existe banco de dados de verdade.

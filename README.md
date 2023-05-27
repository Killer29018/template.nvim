# Template
A plugin for Neovim and Telescope that provides the functionality
to create and use templates

``` lua
-- Load the extension
require('telescope').load_extension('template')

-- Set a keybind to bring up the telescope window
vim.keymap.set('n', '<leader>tT', require'telescope'.extensions.template.template, {})
```

```vimscript
" Use to create a new Template
:TemplateCreate
```

The default keybinds within telescope
```vimscript
<CR> to use the template
<C-D> to delete a template
```

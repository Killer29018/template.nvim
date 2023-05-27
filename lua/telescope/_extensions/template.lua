local sorters = require "telescope.sorters"
local finders = require "telescope.finders"
local pickers = require "telescope.pickers"
local previewers = require "telescope.previewers"
local actions = require "telescope.actions"
local action_state = require "telescope.actions.state"

local themes = require "telescope.themes"
local dropdown_theme = themes.get_dropdown()

function use_template(prompt_bufnr)
    local selected = action_state.get_selected_entry()

    vim.fn.TemplateUse(selected.value)

    actions.close(prompt_bufnr)
end

function remove_template(prompt_bufnr)
    local selected = action_state.get_selected_entry()

    output = vim.fn.TemplateRemove(selected.value)

    if output then
        actions.close(prompt_bufnr)
    end
end

local template = function(opts)
    opts = opts or {}

    pickers.new(opts, {
            prompt_title = "Templates",

            finder = finders.new_table {
                results = vim.fn.TemplateList(),

                entry_maker = function(entry)
                    return {
                        value = entry,
                        ordinal = entry,
                        display = entry
                    }
                end
            },
            
            sorter = sorters.get_generic_fuzzy_sorter({}),

            previewer = previewers.new_buffer_previewer {
                title = "Preview",
                define_preview = function(self, entry, status)
                    local table = vim.fn.TemplateFiles(entry.value)
                    vim.api.nvim_buf_set_lines(self.state.bufnr, 0, -1, false, table)
                end
            },

            attach_mappings = function(prompt_bufnr, map)
                map("i", "<CR>", use_template)
                map("i", "<C-D>", remove_template)

                map("n", "<CR>", use_template)
                map("n", "<C-D>", remove_template)

                return true
            end
        }):find()
end

vim.fn.TemplateList()

return require'telescope'.register_extension {
    setup = function(ext_config, config)
        vim.fn.TemplateList()
    end,
    exports = {
        template = template
    }
}

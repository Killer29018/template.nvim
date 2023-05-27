local sorters = require "telescope.sorters"
local finders = require "telescope.finders"
local pickers = require "telescope.pickers"
local previewers = require "telescope.previewers"
local actions = require "telescope.actions"
local action_state = require "telescope.actions.state"

local themes = require "telescope.themes"
local dropdown_theme = themes.get_dropdown()


--[[
local mini = {
    layout_strategy = "vertical",
    layout_config = {
        height = 0.5,
        width = 0.3,
        prompt_position = "top"
    },
    
    sorting_strategy = "ascending",
}

function enter(prompt_bufnr)
    local selected = action_state.get_selected_entry()
    local cmd = 'colorscheme ' .. selected[1]
    vim.cmd(cmd)
    actions.close(prompt_bufnr)
end


local opts = {
    finder = finders.new_table { "sonokai", "tokyonight", "blue" },
    sorter = sorters.get_generic_fuzzy_sorter({}),

    attach_mappings = function(prompt_bufnr, map)
        map("i", "<CR>", enter)
        return true
    end,
}
local colours = pickers.new(dropdown_theme, opts)

colours:find()
--]]

function use_template(prompt_bufnr)
    local selected = action_state.get_selected_entry()

    vim.fn.TemplateUse(selected[1])

    actions.close(prompt_bufnr)
end

function remove_template(prompt_bufnr)
    local selected = action_state.get_selected_entry()

    output = vim.fn.TemplateRemove(selected[1])

    if output then
        actions.close(prompt_bufnr)
    end
end

local config = {
    finder = finders.new_table(vim.fn.TemplateList()),
    sorter = sorters.get_generic_fuzzy_sorter({}),

    ---[[
    previewer = previewers.new_buffer_previewer {
        title = "Preview",
        define_preview = function (self, entry, status)
            local table = vim.fn.TemplateFiles(entry[1])
            vim.api.nvim_buf_set_lines(self.state.bufnr, 0, -1, false, table)
        end
    },
    --]]

    attach_mappings = function(prompt_bufnr, map)
        map("i", "<CR>", use_template)
        map("i", "<C-D>", remove_template)

        return true
    end,
}

-- local window = pickers.new(opts)

-- window:find()
-- local template_picker = pickers.new(opts)

local template = function(opts)
    opts = opts or {}

    pickers.new(opts, config):find()
end

return require'telescope'.register_extension {
    setup = function(ext_config, config)
    end,
    exports = {
        template = template
    }
}
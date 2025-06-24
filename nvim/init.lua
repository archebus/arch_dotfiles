-- Set <space> as the leader key
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '

-- Install lazy.nvim if not installed
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- Basic settings
vim.opt.number = true          -- Show line numbers
vim.opt.relativenumber = false -- Relative line numbers
vim.opt.tabstop = 4            -- Tab width
vim.opt.softtabstop = 4        -- Tab stop positions when editing
vim.opt.shiftwidth = 4         -- Indentation width
vim.opt.expandtab = true       -- Use spaces instead of tabs
vim.opt.smartindent = true     -- Smart indentation
vim.opt.wrap = false           -- No text wrapping
vim.opt.swapfile = false       -- No swapfile
vim.opt.backup = false         -- No backup file
vim.opt.undodir = vim.fn.stdpath("data") .. "/undodir"
vim.opt.undofile = true        -- Enable persistent undo
vim.opt.hlsearch = false       -- Don't highlight all search matches
vim.opt.incsearch = true       -- Incremental search
vim.opt.termguicolors = true   -- True color support
vim.opt.scrolloff = 8          -- Keep 8 lines above/below cursor
vim.opt.signcolumn = "yes"     -- Always show sign column
vim.opt.updatetime = 50        -- Faster update time
vim.opt.colorcolumn = ""     -- Show column at 80 characters

-- Load plugins from lua/plugins directory
require("lazy").setup("plugins")

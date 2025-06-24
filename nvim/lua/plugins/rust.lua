return {
    {
        -- Mason for installing LSP servers, linters, and formatters
        "williamboman/mason.nvim",
        build = ":MasonUpdate",
        config = function()
            require("mason").setup()
        end,
    },
    {
        "williamboman/mason-lspconfig.nvim",
        dependencies = { "williamboman/mason.nvim" },
        config = function()
            require("mason-lspconfig").setup({
                ensure_installed = { "lua_ls", "pyright" } -- Rust is handled by rustaceanvim
            })
        end,
    },
    {
        -- LSP Configuration
        "neovim/nvim-lspconfig",
        dependencies = {
            "williamboman/mason.nvim",
            "williamboman/mason-lspconfig.nvim",
        },
        config = function()
            -- Basic LSP setup for non-Rust languages
            local lspconfig = require('lspconfig')
            lspconfig.lua_ls.setup {}
            lspconfig.pyright.setup {}
            
            -- Key bindings for LSP functionality
            vim.keymap.set('n', 'K', vim.lsp.buf.hover, { desc = 'Hover Documentation' })
            vim.keymap.set('n', 'gd', vim.lsp.buf.definition, { desc = 'Go to Definition' })
            vim.keymap.set('n', 'gr', vim.lsp.buf.references, { desc = 'Go to References' })
            vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, { desc = 'Code Actions' })
            vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, { desc = 'Rename Symbol' })
        end
    },
    {
        -- Rust-specific development plugin
        "mrcjkb/rustaceanvim",
        version = "^4",  -- Use version 4.0.0 or higher
        ft = { "rust" },  -- Only load for Rust files
        config = function()
            vim.g.rustaceanvim = {
                -- Plugin settings
                tools = {
                    hover_actions = {
                        auto_focus = true,
                    },
                },
                -- Server settings
                server = {
                    settings = {
                        -- Rust-analyzer settings
                        ["rust-analyzer"] = {
                            -- Enable clippy lints
                            check = {
                                command = "clippy",
                                extraArgs = { "--all-features" },
                            },
                            -- Cargo settings
                            cargo = {
                                allFeatures = true,
                                loadOutDirsFromCheck = true,
                            },
                            -- Completion settings
                            completion = {
                                postfix = {
                                    enable = true,
                                },
                            },
                            -- Diagnostics settings
                            diagnostics = {
                                enable = true,
                                experimental = {
                                    enable = true,
                                },
                            },
                        },
                    },
                    on_attach = function(client, bufnr)
                        -- Custom key bindings for Rust
                        local opts = { buffer = bufnr, silent = true }
                        vim.keymap.set("n", "<leader>rh", function()
                            vim.cmd.RustLsp({ 'hover', 'actions' })
                        end, vim.tbl_extend("force", opts, { desc = "Rust Hover Actions" }))
                        
                        vim.keymap.set("n", "<leader>ra", function()
                            vim.cmd.RustLsp('codeAction')
                        end, vim.tbl_extend("force", opts, { desc = "Rust Code Actions" }))
                        
                        vim.keymap.set("n", "<leader>rr", function()
                            vim.cmd.RustLsp('runnables')
                        end, vim.tbl_extend("force", opts, { desc = "Rust Runnables" }))
                    end,
                },
            }
        end
    },
    {
        -- Completion plugin
        "hrsh7th/nvim-cmp",
        dependencies = {
            "hrsh7th/cmp-nvim-lsp",
            "hrsh7th/cmp-buffer",
            "hrsh7th/cmp-path",
            "hrsh7th/cmp-cmdline",
            "L3MON4D3/LuaSnip",
            "saadparwaiz1/cmp_luasnip",
        },
        config = function()
            local cmp = require('cmp')
            local luasnip = require('luasnip')
            
            cmp.setup({
                snippet = {
                    expand = function(args)
                        luasnip.lsp_expand(args.body)
                    end,
                },
                mapping = cmp.mapping.preset.insert({
                    ['<C-b>'] = cmp.mapping.scroll_docs(-4),
                    ['<C-f>'] = cmp.mapping.scroll_docs(4),
                    ['<C-Space>'] = cmp.mapping.complete(),
                    ['<C-e>'] = cmp.mapping.abort(),
                    ['<CR>'] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item
                }),
                sources = cmp.config.sources({
                    { name = 'nvim_lsp' },
                    { name = 'luasnip' },
                    { name = 'buffer' },
                    { name = 'path' },
                }),
            })
        end
    },
    {
        -- Improved syntax highlighting
        "nvim-treesitter/nvim-treesitter",
        build = ":TSUpdate",
        config = function()
            require('nvim-treesitter.configs').setup({
                ensure_installed = { "lua", "rust", "python" },
                highlight = {
                    enable = true,
                },
                indent = {
                    enable = true,
                },
            })
        end
    },
    {
        -- File explorer
        "nvim-tree/nvim-tree.lua",
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
        config = function()
            require("nvim-tree").setup({
                sort_by = "case_sensitive",
                view = {
                    width = 30,
                },
                renderer = {
                    group_empty = true,
                },
                filters = {
                    dotfiles = false,
                },
            })
            vim.keymap.set('n', '<leader>e', ':NvimTreeToggle<CR>', { desc = 'Toggle File Explorer', silent = true })
        end
    },
    {
        -- Fuzzy finder
        "nvim-telescope/telescope.nvim",
        dependencies = {
            "nvim-lua/plenary.nvim",
        },
        config = function()
            require('telescope').setup{}
            vim.keymap.set('n', '<leader>ff', require('telescope.builtin').find_files, { desc = 'Find Files' })
            vim.keymap.set('n', '<leader>fg', require('telescope.builtin').live_grep, { desc = 'Find Text' })
            vim.keymap.set('n', '<leader>fb', require('telescope.builtin').buffers, { desc = 'Find Buffers' })
            vim.keymap.set('n', '<leader>fh', require('telescope.builtin').help_tags, { desc = 'Find Help' })
        end
    },
    {
        -- Status line
        "nvim-lualine/lualine.nvim",
        dependencies = { "nvim-tree/nvim-web-devicons" },
        config = function()
            require('lualine').setup{
                options = {
                    theme = 'gruvbox',
                    component_separators = '|',
                    section_separators = '',
                },
            }
        end
    },
}

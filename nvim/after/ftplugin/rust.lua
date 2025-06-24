-- Configure rustaceanvim
vim.g.rustaceanvim = {
    tools = {
        hover_actions = {
            auto_focus = true,
        },
    },
    server = {
        -- No need to specify cmd since it's in PATH now
        settings = {
            ["rust-analyzer"] = {
                cargo = {
                    allFeatures = true,
                },
                checkOnSave = {
                    command = "clippy",
                },
                diagnostics = {
                    enable = true,
                },
            },
        },
    },
}

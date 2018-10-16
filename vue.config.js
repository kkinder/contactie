module.exports = {
    baseUrl: '/',
    outputDir: __dirname + '/webapp-dist',
    configureWebpack: {
        resolve: {
            alias: {
                '@': __dirname + '/webapp'
            }
        },
        entry: {
            app: './webapp/main.js'
        }
    },
    devServer: {
        host: '127.0.0.1',
        port: 8010,
        proxy: {
            '/api/': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true
            },
        }
    }
}
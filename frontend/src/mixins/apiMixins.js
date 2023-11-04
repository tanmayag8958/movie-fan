let apiMixins = {
    methods: {
        getBaseURL: function () {
            let baseUrl;
            if (process.env.NODE_ENV === 'development') {
                baseUrl = window.location.protocol + '//' +
                    window.location.hostname + `:8000`;
            } else {
                if (!window.location.origin) {
                    window.location.origin = window.location.protocol + '//' + window.location.hostname + (
                        window.location.port ? ':' + window.location.port : ''
                    );
                }
                baseUrl = window.location.origin;
            }
            return baseUrl;
        }
    }
};

export default apiMixins;
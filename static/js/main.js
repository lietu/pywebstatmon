(function () {
    "use strict";

    var log = function () {
        if (console && console.log) {
            var args = Array.prototype.slice.call(arguments);
            args.unshift(new Date());
            console.log.apply(console, args);
        }
    };

    var PyWebStatMon = function () {
        /**
         * The reference returned by setInterval for our updates
         * @type {null}
         */
        this.interval = null;

        /**
         * Milliseconds between updates
         * @type {number}
         */
        this.intervalMsec = 5000;

        /**
         * Are we currently updating or not?
         * @type {boolean}
         */
        this.updating = false;

        /**
         * What URL can we get the data updates from
         * @type {string}
         */
        this.endPoint = '/data.json';

        /**
         * jQuery element that contains our server list
         * @type {null}
         */
        this.$container = null;

        /**
         * URL for loading the server list template from
         * @type {string}
         */
        this.templateUrl = "/static/templates/urls.ejs";

        /**
         * The loaded and compiled template
         */
        this.template = null;
    };

    PyWebStatMon.prototype = {
        /**
         * Start automatic updates of the page
         */
        start: function start() {
            log("Starting up updater");

            this.$container = $('.servers');

            this._load_template(this._start_interval.bind(this));
        },

        /**
         * Load the template and call the given callback once that's done
         * @param {Function} callback
         * @private
         */
        _load_template: function _load_template(callback) {
            if (this.template) {
                callback();
            } else {
                $.get(
                    this.templateUrl,
                    function (html, textStatus) {
                        if (textStatus !== "success") {
                            throw new Error("Failed to load template " + this.templateUrl);
                        }

                        log("Template loaded from " + this.templateUrl);

                        this.template = new EJS({text: html});

                        callback();
                    }.bind(this)
                );
            }
        },

        /**
         * Start an interval for doing our updates
         * @private
         */
        _start_interval: function _start_interval() {
            this.interval = setInterval(this._update.bind(this), this.intervalMsec);
            // Immediately trigger an update, so we can get something out fast
            this._update();
        },

        /**
         * Stop updating the page
         */
        stop: function stop() {
            log("Discontinuing updates");
            if (this.interval) {
                clearInterval(this.interval);
            }
        },

        /**
         * Update data
         * @private
         */
        _update: function _update() {
            if (this.updating) {
                log("Still working on previous update, skipping...");
                return;
            }

            this.updating = true;

            log("Updating data");
            try {
                $.ajax({
                    dataType: "json",
                    url: this.endPoint,
                    success: function (data, textStatus, xhrRequest) {
                        if (textStatus === "success") {
                            var viewData = {
                                results: data
                            };

                            var html = this.template.render(viewData);

                            this.$container.html(html);
                        } else {
                            log("Error fetching data .. " + textStatus);
                        }

                        this.updating = false;
                    }.bind(this),
                    error: function() {
                        log("Error fetching data .. ", arguments);

                        this.updating = false;

                    }.bind(this)
                });
            } catch (e) {
                log("Error fetching data .. " + e);

                this.updating = false;
            }
        }
    };


    $(function () {
        var app = new PyWebStatMon();
        app.start();
    })
})();
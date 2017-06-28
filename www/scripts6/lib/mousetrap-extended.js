define(["mousetrap"], function(mousetrap){

// see https://github.com/ccampbell/mousetrap/tree/master/plugins/bind-dictionary
/**
 * Overwrites default mousetrap.bind method to optionally accept
 * an object to bind multiple key events in a single call
 *
 * You can pass it in like:
 *
 * mousetrap.bind({
 *     'a': function() { console.log('a'); },
 *     'b': function() { console.log('b'); }
 * });
 *
 * And can optionally pass in 'keypress', 'keydown', or 'keyup'
 * as a second argument
 *
 */
/* global mousetrap:true */
(function(mousetrap) {
    var _oldBind = mousetrap.prototype.bind;
    var args;

    mousetrap.prototype.bind = function() {
        var self = this;
        args = arguments;

        // normal call
        if (typeof args[0] == 'string' || args[0] instanceof Array) {
            return _oldBind.call(self, args[0], args[1], args[2]);
        }

        // object passed in
        for (var key in args[0]) {
            if (args[0].hasOwnProperty(key)) {
                _oldBind.call(self, key, args[0][key], args[1]);
            }
        }
    };

    mousetrap.init();
}) (mousetrap);

// see https://github.com/ccampbell/mousetrap/tree/master/plugins/global-bind
/**
 * adds a bindGlobal method to mousetrap that allows you to
 * bind specific keyboard shortcuts that will still work
 * inside a text input field
 *
 * usage:
 * mousetrap.bindGlobal('ctrl+s', _saveChanges);
 */
/* global mousetrap:true */
(function(mousetrap) {
    var _globalCallbacks = {};
    var _originalStopCallback = mousetrap.prototype.stopCallback;

    mousetrap.prototype.stopCallback = function(e, element, combo, sequence) {
        var self = this;

        if (self.paused) {
            return true;
        }

        if (_globalCallbacks[combo] || _globalCallbacks[sequence]) {
            return false;
        }

        return _originalStopCallback.call(self, e, element, combo);
    };

    mousetrap.prototype.bindGlobal = function(keys, callback, action) {
        var self = this;
        self.bind(keys, callback, action);

        if (keys instanceof Array) {
            for (var i = 0; i < keys.length; i++) {
                _globalCallbacks[keys[i]] = true;
            }
            return;
        }

        _globalCallbacks[keys] = true;
    };

    mousetrap.init();
}) (mousetrap);





return mousetrap

}) // end define

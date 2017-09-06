
(function(tagger) {
  if (typeof define === 'function' && define.amd) {
    define(function(require, exports, module) { tagger(require('riot'), require, exports, module)})
  } else if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    tagger(require('riot'), require, exports, module)
  } else {
    tagger(window.riot)
  }
})(function(riot, require, exports, module) {
riot.tag2('urlpath-autocomplete', '<yield></yield> <ol if="{open}" class="urlpath-autocomplete-options"> <li each="{item, index in items.results}" onmouseover="{parent.selectingByMouse}" onclick="{parent.selectByMouse}" class="{\'selecting\': selecting == index}">{item.name}</li> </ol> <span if="{textChanged}" onclick="{this.undoTextChanges}">Reset changes</span>', '', '', function(opts) {


    this.inputEl = void(0);
    this.url = void(0);
    this.history = {};
    this.items = {};
    this.open = false;
    this.lastKey = [];
    this.submitKeys = this.opts.submitKeys || [
        9,
        13
    ];
    this.navigationKeys = this.opts.navigationKeys || [
        38,
        40
    ];
    this.cancelKeys = this.opts.cancelKeys || [
        27
    ];
    this.selecting = -1;

    this.text = '';
    this.originalText = '';
    this.textChanged = false;
    this.undoTextChanges = function(event) {
        event.stopPropagation();
        event.preventDefault();
        this.text = this.originalText;
        this.inputEl.val(this.text);
        this.inputEl.focus();
        this.trigger('cancel', event);
    }.bind(this)

    this.on('mount', function(){
        this.inputEl = django.jQuery('input[type="text"]', this.root).eq(0).attr("autocomplete", "off");
        this.originalText = this.inputEl.val().trim();

        const self = this;
        this.inputEl.on("keydown", function(event) {
            self.lastKey.push(event.which);

            if (self.submitKeys.indexOf(event.which) > -1 && self.selecting !== -1 && self.open) {
                event.preventDefault();
            }

            if (self.navigationKeys.indexOf(event.which) > -1 && self.open) {
                event.preventDefault();
                return self.trigger('navigate', event);
            }
        });
        this.inputEl.on("keyup", function(event) {
            self.text = self.inputEl.val().trim();
            if (!self.text) {
                return self.trigger('cancel', event);
            }

            if (self.submitKeys.indexOf(event.which) > -1 && self.open) {
                if (self.selected !== -1) {
                    return self.trigger('select', event);
                } else {
                    return self.trigger('cancel', event);
                }
            }
            if (self.cancelKeys.indexOf(event.which) > -1 && self.open) {
                event.preventDefault();
                return self.trigger('cancel', event);
            }
            if (self.text !== self.originalText) {
                return self.trigger('text', event);
            }
        });
        this.inputEl.on("blur", function(evt) {

            if (self.open) {
                self.text = django.jQuery(this).val();
                if (self.selecting == -1) {
                    self.trigger('cancel', evt);
                }
            }
        });
    });
    this.on('navigate', function(event) {
        var selecting;
        if (event.which === 38) {
            selecting = this.selecting - 1;
        } else {
            selecting = this.selecting + 1;
        }

        if (selecting >= this.items.results.length) {
            selecting = 0;
        } else if (selecting < 0) {
            selecting = this.items.results.length - 1;
        }
        this.selecting = selecting;
        this.update();
    });
    this.on('text', function(event) {
        const text = this.text;

        if (this.history[text] !== void(0) && this.history[text].results) {
            this.items = this.history[text]
            this.update();
        } else {
            const self = this;
            django.jQuery.getJSON(this.opts.url, {'q': text})
            .fail(function(data) {
                self.history[text] = data;
            }).fail(function(data) {
                self.history[text] = void(0);
            })
            .always(function(data) {
                self.items = data;
                self.update();
            });
        }
    });
    this.selectingByMouse = function(event) {
        this.selecting = event.item.index;
    }.bind(this)
    this.selectByMouse = function(event) {
        this.selecting = event.item.index;
        this.trigger('select', event);
    }.bind(this);
    this.on('select', function(event) {
        const selection = this.items.results[this.selecting];

        if (selection !== void(0)) {
            this.inputEl.val(selection.name);
            this.inputEl.focus();
        }
        this.trigger('cancel', event);
    });
    this.on('cancel', function(event) {
        this.items = {};
        this.selecting = -1;
        this.update();
    });
    this.on('update', function() {
        this.open = this.items.results && this.items.results.length > 0;
        this.textChanged = this.text !== this.originalText;
    });
});
});
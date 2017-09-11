
(function(tagger) {
  if (typeof define === 'function' && define.amd) {
    define(function(require, exports, module) { tagger(require('riot'), require, exports, module)})
  } else if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    tagger(require('riot'), require, exports, module)
  } else {
    tagger(window.riot)
  }
})(function(riot, require, exports, module) {
riot.tag2('urlpath-autocomplete', '<yield></yield> <ol if="{open}" class="urlpath-autocomplete-options" onmouseout="{unselectIfMousing}"> <li each="{item, index in items.results}" onmouseover="{parent.selectingByMouse}" onclick="{parent.selectByMouse}" class="{\'selecting\': selecting == index}"> <em>{item.parts.prefix}</em> <b>{item.parts.match}</b> <em>{item.parts.suffix}</em></li> </ol> <span if="{textChanged}" onclick="{this.undoTextChanges}">Reset changes</span>', '', '', function(opts) {


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
    this.mousing = false;

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

        const tag = this;
        this.inputEl.on("keydown", function(event) {
            tag.lastKey.push(event.which);

            if (tag.submitKeys.indexOf(event.which) > -1 && tag.selecting !== -1 && tag.open) {
                event.preventDefault();
            }

            if (tag.navigationKeys.indexOf(event.which) > -1 && tag.open) {
                event.preventDefault();
                return tag.trigger('navigate', event);
            }
        });
        this.inputEl.on("keyup", function(event) {
            tag.text = tag.inputEl.val().trim();
            if (!tag.text) {
                return tag.trigger('cancel', event);
            }

            if (tag.submitKeys.indexOf(event.which) > -1 && tag.open) {
                if (tag.selected !== -1) {
                    return tag.trigger('select', event);
                } else {
                    return tag.trigger('cancel', event);
                }
            }
            if (tag.cancelKeys.indexOf(event.which) > -1 && tag.open) {
                event.preventDefault();
                return tag.trigger('cancel', event);
            }
            if (tag.text !== tag.originalText) {
                return tag.trigger('text', event);
            }
        });
        this.inputEl.on("blur", function(evt) {

            if (tag.open) {
                tag.text = django.jQuery(this).val();
                tag.trigger('cancel', evt);
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
        this.mousing = false;
        this.selecting = selecting;
        this.update();
    });
    this.on('text', function(event) {
        const text = this.text;

        if (this.history[text] !== void(0) && this.history[text].results) {
            this.items = this.history[text]
            this.update();
        } else {
            const tag = this;
            django.jQuery.getJSON(this.opts.url, {'q': text})
            .done(function(data) {
                tag.history[text] = data;
            })
            .fail(function(data) {
                tag.history[text] = void(0);
            })
            .always(function(data) {
                tag.items = data;
                tag.update();
            });
        }
    });
    this.selectingByMouse = function(event) {
        this.mousing = true;
        this.selecting = event.item.index;
    }.bind(this)
    this.unselectIfMousing = function(event) {
        if (this.mousing === true) {
            this.mousing = false;
            this.selecting = -1;
        }
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
        this.mousing = false;
        this.selecting = -1;
        this.update();
    });
    this.on('update', function() {
        this.open = this.items.results && this.items.results.length > 0;
        this.textChanged = this.text !== this.originalText;
    });
});
});
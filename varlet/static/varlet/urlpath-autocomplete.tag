<urlpath-autocomplete>
    <yield />
    <ol if={open} class="urlpath-autocomplete-options">
        <li each={item, index in items.results} onmouseover={parent.selectingByMouse} onclick={parent.selectByMouse} class={'selecting': selecting == index}>{ item.name }</li>
    </ol>
    <span if={textChanged} onclick={this.undoTextChanges}>Reset changes</span>

    <style>
        :scope {
            display: inline-block;
            position: absolute;
            z-index: 1000;
            min-width: 20em;
            max-width: calc(100% - 260px);
            width: 100%;
            box-sizing: border-box;
        }

        :scope input {
            width: 100%;
            box-sizing: border-box;
        }

        :scope ol {
            box-sizing: border-box;
            margin: -3px 0 0 0;
            padding: 0.5em 0;
            list-style: none;
            background-color: #FFF;
            border: 1px solid #999;
            border-top: 1px solid #EEE;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            min-width: 100%;
            position: absolute;
            z-index: 1001;
        }

        :scope ol li {
            background-color: #FFF;
            padding: 5px 6px;
            box-sizing: border-box;
        }

        :scope ol li.selecting {
            background-color: #79aec8;
            cursor: pointer;
            color: #FFF;
            background-image: url("../admin/img/tooltag-arrowright.svg");
            background-repeat: no-repeat;
            background-position: right 7px center;
        }

        :scope ol li:focus,
        [data-is="urlpath-autocomplete"] ol li:focus {
            background-color: #417690;
        }
        :scope span {
            box-sizing: border-box;
            position: absolute;
            top: 0;
            right: 0;
            display: inline-block;
            padding: 7px 6px;
            color: #79aec8;
            cursor: pointer;
            font-weight: 400;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 4px;
        }
        :scope span:hover {
            background-color: #417690;
            color: #FFF;
        }
        :scope ol + span {
            padding-top: 5px;
            padding-bottom: 5px;
        }
    </style>

    this.inputEl = void(0);
    this.url = void(0);
    this.history = {};
    this.items = {};
    this.open = false;
    this.lastKey = [];
    this.submitKeys = this.opts.submitKeys || [
        9,  // tab
        13 // enter
    ];
    this.navigationKeys = this.opts.navigationKeys || [
        38, // up
        40 // down
    ];
    this.cancelKeys = this.opts.cancelKeys || [
        27 // escape
    ];
    this.selecting = -1;

    this.text = '';
    this.originalText = '';
    this.textChanged = false;
    undoTextChanges(event) {
        event.stopPropagation();
        event.preventDefault();
        this.text = this.originalText;
        this.inputEl.val(this.text);
        this.inputEl.focus();
        this.trigger('cancel', event);
    }

    this.on('mount', function(){
        this.inputEl = django.jQuery('input[type="text"]', this.root).eq(0).attr("autocomplete", "off");
        this.originalText = this.inputEl.val().trim();

        const self = this;
        this.inputEl.on("keydown", function(event) {
            self.lastKey.push(event.which);
            // you cannot prevent the enter on a form field from doing its default
            // action (submitting on ENTER etc) on keyup, so we have to do it here.
            if (self.submitKeys.indexOf(event.which) > -1 && self.selecting !== -1 && self.open) {
                event.preventDefault();
            }
            // By listening for up/down here instead of on keyup, we can just
            // hold down the key and keep firing to get a new selection.
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
            // if its open and we press TAB, or ENTER etc, and we have
            // selected an item either by the keyboard navigation keys or by
            // the mouse, then select it.
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
            // when tabbing out, or clicking elsewhere, dismiss the autocompleter.
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
        // turn the choices into a ring, wrapping around when you go past the
        // end or before the beginning.
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
        // check whether we can re-fill this from local history (ie: pressed backspace)
        // having already typed past it.
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
    selectingByMouse(event) {
        this.selecting = event.item.index;
    }
    selectByMouse(event) {
        this.selecting = event.item.index;
        this.trigger('select', event);
    };
    this.on('select', function(event) {
        const selection = this.items.results[this.selecting];
        // do not allow selecting if we previously had, say, index 3 highlighted
        // but now there are only 2 items to choose from, and the user pressed
        // one of the submitKeys hoping to pre-fill
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
</urlpath-autocomplete>

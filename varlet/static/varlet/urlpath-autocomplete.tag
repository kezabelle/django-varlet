<urlpath-autocomplete>
    <yield />
    <ol if={open} class="urlpath-autocomplete-options" onmouseout={unselectIfMousing}>
        <li each={item, index in items.results} onmouseover={parent.selectingByMouse} onclick={parent.selectByMouse} class={'selecting': selecting == index}>
        <em>{ item.parts.prefix }</em>
        <b>{ item.parts.match }</b>
        <em>{ item.parts.suffix }</em></li>
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
            font-size: 0;
            box-sizing: border-box;
        }
        :scope ol li em {
            font-size: 13px;
            font-style: normal;
            color: #417690;
            border-bottom: 1px dotted #79aec8;
        }
        :scope ol li b {
            font-size: 13px;
            font-weight: 400;
            color: #787878;
        }

        :scope ol li.selecting {
            background-image: url("../admin/img/tooltag-arrowright.svg");
            background-color: #79aec8;
            text-shadow: 2px 2px 2px #417690;
            cursor: pointer;
            background-repeat: no-repeat;
            background-position: right 7px center;
        }

        :scope ol li:focus {
            background-color: #417690;
        }
        :scope ol li.selecting em,
        :scope ol li.selecting b,
        :scope ol li:focus em,
        :scope ol li:focus b {
            color: #FFF;
            border-bottom: 1px solid #79aec8;
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
            -webkit-transition: padding-top 300ms ease-in-out,  padding-bottom 300ms ease-in-out;
            -moz-transition: padding-top 300ms ease-in-out,  padding-bottom 300ms ease-in-out;
            -ms-transition: padding-top 300ms ease-in-out,  padding-bottom 300ms ease-in-out;
            -o-transition: padding-top 300ms ease-in-out,  padding-bottom 300ms ease-in-out;
            transition: padding-top 300ms ease-in-out,  padding-bottom 300ms ease-in-out;
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
    this.mousing = false;

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

        const tag = this;
        this.inputEl.on("keydown", function(event) {
            tag.lastKey.push(event.which);
            // you cannot prevent the enter on a form field from doing its default
            // action (submitting on ENTER etc) on keyup, so we have to do it here.
            if (tag.submitKeys.indexOf(event.which) > -1 && tag.selecting !== -1 && tag.open) {
                event.preventDefault();
            }
            // By listening for up/down here instead of on keyup, we can just
            // hold down the key and keep firing to get a new selection.
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
            // if its open and we press TAB, or ENTER etc, and we have
            // selected an item either by the keyboard navigation keys or by
            // the mouse, then select it.
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
            // when tabbing out, or clicking elsewhere, dismiss the autocompleter.
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
        // turn the choices into a ring, wrapping around when you go past the
        // end or before the beginning.
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
        // check whether we can re-fill this from local history (ie: pressed backspace)
        // having already typed past it.
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
    selectingByMouse(event) {
        this.mousing = true;
        this.selecting = event.item.index;
    }
    unselectIfMousing(event) {
        if (this.mousing === true) {
            this.mousing = false;
            this.selecting = -1;
        }
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
        this.mousing = false;
        this.selecting = -1;
        this.update();
    });
    this.on('update', function() {
        this.open = this.items.results && this.items.results.length > 0;
        this.textChanged = this.text !== this.originalText;
    });
</urlpath-autocomplete>

(function () {

var Finder = window.Finder = function (obj) {

    this.$view = $(Finder.template());
    this.$address = this.$view.find('.address');
    this.$address_with_zipcode = this.$view.find('.address-with-zipcode');
    this.$loader = this.$view.find('.loader');

    this._units_re = /[縣市鄉鎮市區村里路段街巷弄號樓]/;
    this._model = {};
    this.model(obj || {});

    this.$address.on('input',
        _.bind(this.controller, this, 'address-input')
    );

    this.$address_with_zipcode.on('click',
        _.bind(this.controller, this, 'address-with-zipcode-click')
    );

};

Finder.template = _.template(
    '<article class="finder">'+
        '<input class="address" placeholder="請在上面這欄輸入地址" value="">'+
        '<div class="address-with-zipcode-wrapper">'+
            '<input class="address-with-zipcode" placeholder="郵遞區號會出現在這邊" value="">'+
            '<img class="loader" src="/static/loader.gif">'+
        '</div>'+
    '</article>'
);

Finder.prototype.view = function (model_changed) {

    if (model_changed.loading !== undefined) {
        this.$view.toggleClass('loading', model_changed.loading);
    }

    if (
        model_changed.zipcode != undefined ||
        model_changed.address != undefined
    ) {
        var zipcode = this._model.zipcode || '';
        var address = this._model.address || '';
        this.$address_with_zipcode.val(zipcode + (zipcode ? ' ' : '') + address)
    }

};

Finder.cache = {};

Finder.prototype.model = function (model_changed) {

    var _this = this;

    // update the internal model
    $.each(model_changed, function (key, value) {
        if (_this._model[key] === value) {
            delete model_changed[key];
        } else {
            _this._model[key] = value;
        }
    });

    if (
        model_changed.address !== undefined &&
        this._units_re.test(model_changed.address.slice(-1))
    ) {
        // try cache or send request
        var zipcode = Finder.cache[model_changed.address];
        if (zipcode !== undefined) {
            _this.model({zipcode: zipcode});
        } else {
            _this.model({loading: true});
            $.getJSON('/api/find', {
                address: model_changed.address
            }).done(function (resp) {
                var zipcode = resp.result;
                Finder.cache[model_changed.address] = zipcode;
                _this.model({zipcode: zipcode});
            }).always(function () {
                _this.model({loading: false});
            });
        }
    } else if (model_changed.address === '') {
        _this.model({zipcode: ''});
    }

    this.view(model_changed);

};

Finder.prototype.controller = function (event_name) {

    switch (event_name) {

        case 'address-input':
            this.model({address: this.$address.val()});
            break;

        case 'address-with-zipcode-click':
            this.$address_with_zipcode.select();
            break
    }

};

})();

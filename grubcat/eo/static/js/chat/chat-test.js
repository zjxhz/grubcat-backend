(function ($) {
    var
        defaults = {className: 'autosizejs', append: '', callback: false}, hidden = 'hidden', borderBox = 'border-box', lineHeight = 'lineHeight', supportsScrollHeight, copy = '<textarea tabindex="-1" style="position:absolute; top:-999px; left:0; right:auto; bottom:auto; border:0; -moz-box-sizing:content-box; -webkit-box-sizing:content-box; box-sizing:content-box; word-wrap:break-word; height:0 !important; min-height:0 !important; overflow:hidden;"/>', copyStyle = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'letterSpacing', 'textTransform', 'wordSpacing', 'textIndent'], oninput = 'oninput', onpropertychange = 'onpropertychange', mirrored, mirror = $(copy).data('autosize', true)[0];
    mirror.style.lineHeight = '99px';
    if ($(mirror).css(lineHeight) === '99px') {
        copyStyle.push(lineHeight);
    }
    mirror.style.lineHeight = '';
    $.fn.autosize = function (options) {
        options = $.extend({}, defaults, options || {});
        if (mirror.parentNode !== document.body) {
            $(document.body).append(mirror);
            mirror.value = "\n\n\n";
            mirror.scrollTop = 9e4;
            supportsScrollHeight = mirror.scrollHeight === mirror.scrollTop + mirror.clientHeight;
        }
        return this.each(function () {
            var
                ta = this, $ta = $(ta), minHeight, active, resize, boxOffset = 0, callback = $.isFunction(options.callback);
            if ($ta.data('autosize')) {
                return;
            }
            if ($ta.css('box-sizing') === borderBox || $ta.css('-moz-box-sizing') === borderBox || $ta.css('-webkit-box-sizing') === borderBox) {
                boxOffset = $ta.outerHeight() - $ta.height();
            }
            minHeight = Math.max(parseInt($ta.css('minHeight'), 10) - boxOffset, $ta.height());
            resize = ($ta.css('resize') === 'none' || $ta.css('resize') === 'vertical') ? 'none' : 'horizontal';
            $ta.css({overflow: hidden, overflowY: hidden, wordWrap: 'break-word', resize: resize}).data('autosize', true);
            function initMirror() {
                mirrored = ta;
                mirror.className = options.className;
                $.each(copyStyle, function (i, val) {
                    mirror.style[val] = $ta.css(val);
                });
            }

            function adjust() {
                var height, overflow, original;
                if (mirrored !== ta) {
                    initMirror();
                }
                if (!active) {
                    active = true;
                    mirror.value = ta.value + options.append;
                    mirror.style.overflowY = ta.style.overflowY;
                    original = parseInt(ta.style.height, 10);
                    mirror.style.width = Math.max($ta.width(), 0) + 'px';
                    if (supportsScrollHeight) {
                        height = mirror.scrollHeight;
                    } else {
                        mirror.scrollTop = 0;
                        mirror.scrollTop = 9e4;
                        height = mirror.scrollTop;
                    }
                    var maxHeight = parseInt($ta.css('maxHeight'), 10);
                    maxHeight = maxHeight && maxHeight > 0 ? maxHeight : 9e4;
                    if (height > maxHeight) {
                        height = maxHeight;
                        overflow = 'scroll';
                    } else if (height < minHeight) {
                        height = minHeight;
                    }
                    height += boxOffset;
                    ta.style.overflowY = overflow || hidden;
                    if (original !== height) {
                        ta.style.height = height + 'px';
                        if (callback) {
                            options.callback.call(ta);
                        }
                    }
                    setTimeout(function () {
                        active = false;
                    }, 1);
                }
            }

            if (onpropertychange in ta) {
                if (oninput in ta) {
                    ta[oninput] = ta.onkeyup = adjust;
                } else {
                    ta[onpropertychange] = adjust;
                }
            } else {
                ta[oninput] = adjust;
            }
            $(window).on('resize', function () {
                active = false;
                adjust();
            });
            $ta.on('autosize', function () {
                active = false;
                adjust();
            });
            adjust();
        });
    };
}(window.jQuery || window.Zepto));
(function () {
    var root = this;
    var previousUnderscore = root._;
    var breaker = {};
    var ArrayProto = Array.prototype, ObjProto = Object.prototype, FuncProto = Function.prototype;
    var push = ArrayProto.push, slice = ArrayProto.slice, concat = ArrayProto.concat, toString = ObjProto.toString, hasOwnProperty = ObjProto.hasOwnProperty;
    var
        nativeForEach = ArrayProto.forEach, nativeMap = ArrayProto.map, nativeReduce = ArrayProto.reduce, nativeReduceRight = ArrayProto.reduceRight, nativeFilter = ArrayProto.filter, nativeEvery = ArrayProto.every, nativeSome = ArrayProto.some, nativeIndexOf = ArrayProto.indexOf, nativeLastIndexOf = ArrayProto.lastIndexOf, nativeIsArray = Array.isArray, nativeKeys = Object.keys, nativeBind = FuncProto.bind;
    var _ = function (obj) {
        if (obj instanceof _)return obj;
        if (!(this instanceof _))return new _(obj);
        this._wrapped = obj;
    };
    if (typeof exports !== 'undefined') {
        if (typeof module !== 'undefined' && module.exports) {
            exports = module.exports = _;
        }
        exports._ = _;
    } else {
        root._ = _;
    }
    _.VERSION = '1.4.4';
    var each = _.each = _.forEach = function (obj, iterator, context) {
        if (obj == null)return;
        if (nativeForEach && obj.forEach === nativeForEach) {
            obj.forEach(iterator, context);
        } else if (obj.length === +obj.length) {
            for (var i = 0, l = obj.length; i < l; i++) {
                if (iterator.call(context, obj[i], i, obj) === breaker)return;
            }
        } else {
            for (var key in obj) {
                if (_.has(obj, key)) {
                    if (iterator.call(context, obj[key], key, obj) === breaker)return;
                }
            }
        }
    };
    _.map = _.collect = function (obj, iterator, context) {
        var results = [];
        if (obj == null)return results;
        if (nativeMap && obj.map === nativeMap)return obj.map(iterator, context);
        each(obj, function (value, index, list) {
            results[results.length] = iterator.call(context, value, index, list);
        });
        return results;
    };
    var reduceError = 'Reduce of empty array with no initial value';
    _.reduce = _.foldl = _.inject = function (obj, iterator, memo, context) {
        var initial = arguments.length > 2;
        if (obj == null)obj = [];
        if (nativeReduce && obj.reduce === nativeReduce) {
            if (context)iterator = _.bind(iterator, context);
            return initial ? obj.reduce(iterator, memo) : obj.reduce(iterator);
        }
        each(obj, function (value, index, list) {
            if (!initial) {
                memo = value;
                initial = true;
            } else {
                memo = iterator.call(context, memo, value, index, list);
            }
        });
        if (!initial)throw new TypeError(reduceError);
        return memo;
    };
    _.reduceRight = _.foldr = function (obj, iterator, memo, context) {
        var initial = arguments.length > 2;
        if (obj == null)obj = [];
        if (nativeReduceRight && obj.reduceRight === nativeReduceRight) {
            if (context)iterator = _.bind(iterator, context);
            return initial ? obj.reduceRight(iterator, memo) : obj.reduceRight(iterator);
        }
        var length = obj.length;
        if (length !== +length) {
            var keys = _.keys(obj);
            length = keys.length;
        }
        each(obj, function (value, index, list) {
            index = keys ? keys[--length] : --length;
            if (!initial) {
                memo = obj[index];
                initial = true;
            } else {
                memo = iterator.call(context, memo, obj[index], index, list);
            }
        });
        if (!initial)throw new TypeError(reduceError);
        return memo;
    };
    _.find = _.detect = function (obj, iterator, context) {
        var result;
        any(obj, function (value, index, list) {
            if (iterator.call(context, value, index, list)) {
                result = value;
                return true;
            }
        });
        return result;
    };
    _.filter = _.select = function (obj, iterator, context) {
        var results = [];
        if (obj == null)return results;
        if (nativeFilter && obj.filter === nativeFilter)return obj.filter(iterator, context);
        each(obj, function (value, index, list) {
            if (iterator.call(context, value, index, list))results[results.length] = value;
        });
        return results;
    };
    _.reject = function (obj, iterator, context) {
        return _.filter(obj, function (value, index, list) {
            return!iterator.call(context, value, index, list);
        }, context);
    };
    _.every = _.all = function (obj, iterator, context) {
        iterator || (iterator = _.identity);
        var result = true;
        if (obj == null)return result;
        if (nativeEvery && obj.every === nativeEvery)return obj.every(iterator, context);
        each(obj, function (value, index, list) {
            if (!(result = result && iterator.call(context, value, index, list)))return breaker;
        });
        return!!result;
    };
    var any = _.some = _.any = function (obj, iterator, context) {
        iterator || (iterator = _.identity);
        var result = false;
        if (obj == null)return result;
        if (nativeSome && obj.some === nativeSome)return obj.some(iterator, context);
        each(obj, function (value, index, list) {
            if (result || (result = iterator.call(context, value, index, list)))return breaker;
        });
        return!!result;
    };
    _.contains = _.include = function (obj, target) {
        if (obj == null)return false;
        if (nativeIndexOf && obj.indexOf === nativeIndexOf)return obj.indexOf(target) != -1;
        return any(obj, function (value) {
            return value === target;
        });
    };
    _.invoke = function (obj, method) {
        var args = slice.call(arguments, 2);
        var isFunc = _.isFunction(method);
        return _.map(obj, function (value) {
            return(isFunc ? method : value[method]).apply(value, args);
        });
    };
    _.pluck = function (obj, key) {
        return _.map(obj, function (value) {
            return value[key];
        });
    };
    _.where = function (obj, attrs, first) {
        if (_.isEmpty(attrs))return first ? null : [];
        return _[first ? 'find' : 'filter'](obj, function (value) {
            for (var key in attrs) {
                if (attrs[key] !== value[key])return false;
            }
            return true;
        });
    };
    _.findWhere = function (obj, attrs) {
        return _.where(obj, attrs, true);
    };
    _.max = function (obj, iterator, context) {
        if (!iterator && _.isArray(obj) && obj[0] === +obj[0] && obj.length < 65535) {
            return Math.max.apply(Math, obj);
        }
        if (!iterator && _.isEmpty(obj))return-Infinity;
        var result = {computed: -Infinity, value: -Infinity};
        each(obj, function (value, index, list) {
            var computed = iterator ? iterator.call(context, value, index, list) : value;
            computed >= result.computed && (result = {value: value, computed: computed});
        });
        return result.value;
    };
    _.min = function (obj, iterator, context) {
        if (!iterator && _.isArray(obj) && obj[0] === +obj[0] && obj.length < 65535) {
            return Math.min.apply(Math, obj);
        }
        if (!iterator && _.isEmpty(obj))return Infinity;
        var result = {computed: Infinity, value: Infinity};
        each(obj, function (value, index, list) {
            var computed = iterator ? iterator.call(context, value, index, list) : value;
            computed < result.computed && (result = {value: value, computed: computed});
        });
        return result.value;
    };
    _.shuffle = function (obj) {
        var rand;
        var index = 0;
        var shuffled = [];
        each(obj, function (value) {
            rand = _.random(index++);
            shuffled[index - 1] = shuffled[rand];
            shuffled[rand] = value;
        });
        return shuffled;
    };
    var lookupIterator = function (value) {
        return _.isFunction(value) ? value : function (obj) {
            return obj[value];
        };
    };
    _.sortBy = function (obj, value, context) {
        var iterator = lookupIterator(value);
        return _.pluck(_.map(obj,function (value, index, list) {
            return{value: value, index: index, criteria: iterator.call(context, value, index, list)};
        }).sort(function (left, right) {
            var a = left.criteria;
            var b = right.criteria;
            if (a !== b) {
                if (a > b || a === void 0)return 1;
                if (a < b || b === void 0)return-1;
            }
            return left.index < right.index ? -1 : 1;
        }), 'value');
    };
    var group = function (obj, value, context, behavior) {
        var result = {};
        var iterator = lookupIterator(value || _.identity);
        each(obj, function (value, index) {
            var key = iterator.call(context, value, index, obj);
            behavior(result, key, value);
        });
        return result;
    };
    _.groupBy = function (obj, value, context) {
        return group(obj, value, context, function (result, key, value) {
            (_.has(result, key) ? result[key] : (result[key] = [])).push(value);
        });
    };
    _.countBy = function (obj, value, context) {
        return group(obj, value, context, function (result, key) {
            if (!_.has(result, key))result[key] = 0;
            result[key]++;
        });
    };
    _.sortedIndex = function (array, obj, iterator, context) {
        iterator = iterator == null ? _.identity : lookupIterator(iterator);
        var value = iterator.call(context, obj);
        var low = 0, high = array.length;
        while (low < high) {
            var mid = (low + high) >>> 1;
            iterator.call(context, array[mid]) < value ? low = mid + 1 : high = mid;
        }
        return low;
    };
    _.toArray = function (obj) {
        if (!obj)return[];
        if (_.isArray(obj))return slice.call(obj);
        if (obj.length === +obj.length)return _.map(obj, _.identity);
        return _.values(obj);
    };
    _.size = function (obj) {
        if (obj == null)return 0;
        return(obj.length === +obj.length) ? obj.length : _.keys(obj).length;
    };
    _.first = _.head = _.take = function (array, n, guard) {
        if (array == null)return void 0;
        return(n != null) && !guard ? slice.call(array, 0, n) : array[0];
    };
    _.initial = function (array, n, guard) {
        return slice.call(array, 0, array.length - ((n == null) || guard ? 1 : n));
    };
    _.last = function (array, n, guard) {
        if (array == null)return void 0;
        if ((n != null) && !guard) {
            return slice.call(array, Math.max(array.length - n, 0));
        } else {
            return array[array.length - 1];
        }
    };
    _.rest = _.tail = _.drop = function (array, n, guard) {
        return slice.call(array, (n == null) || guard ? 1 : n);
    };
    _.compact = function (array) {
        return _.filter(array, _.identity);
    };
    var flatten = function (input, shallow, output) {
        each(input, function (value) {
            if (_.isArray(value)) {
                shallow ? push.apply(output, value) : flatten(value, shallow, output);
            } else {
                output.push(value);
            }
        });
        return output;
    };
    _.flatten = function (array, shallow) {
        return flatten(array, shallow, []);
    };
    _.without = function (array) {
        return _.difference(array, slice.call(arguments, 1));
    };
    _.uniq = _.unique = function (array, isSorted, iterator, context) {
        if (_.isFunction(isSorted)) {
            context = iterator;
            iterator = isSorted;
            isSorted = false;
        }
        var initial = iterator ? _.map(array, iterator, context) : array;
        var results = [];
        var seen = [];
        each(initial, function (value, index) {
            if (isSorted ? (!index || seen[seen.length - 1] !== value) : !_.contains(seen, value)) {
                seen.push(value);
                results.push(array[index]);
            }
        });
        return results;
    };
    _.union = function () {
        return _.uniq(concat.apply(ArrayProto, arguments));
    };
    _.intersection = function (array) {
        var rest = slice.call(arguments, 1);
        return _.filter(_.uniq(array), function (item) {
            return _.every(rest, function (other) {
                return _.indexOf(other, item) >= 0;
            });
        });
    };
    _.difference = function (array) {
        var rest = concat.apply(ArrayProto, slice.call(arguments, 1));
        return _.filter(array, function (value) {
            return!_.contains(rest, value);
        });
    };
    _.zip = function () {
        var args = slice.call(arguments);
        var length = _.max(_.pluck(args, 'length'));
        var results = new Array(length);
        for (var i = 0; i < length; i++) {
            results[i] = _.pluck(args, "" + i);
        }
        return results;
    };
    _.object = function (list, values) {
        if (list == null)return{};
        var result = {};
        for (var i = 0, l = list.length; i < l; i++) {
            if (values) {
                result[list[i]] = values[i];
            } else {
                result[list[i][0]] = list[i][1];
            }
        }
        return result;
    };
    _.indexOf = function (array, item, isSorted) {
        if (array == null)return-1;
        var i = 0, l = array.length;
        if (isSorted) {
            if (typeof isSorted == 'number') {
                i = (isSorted < 0 ? Math.max(0, l + isSorted) : isSorted);
            } else {
                i = _.sortedIndex(array, item);
                return array[i] === item ? i : -1;
            }
        }
        if (nativeIndexOf && array.indexOf === nativeIndexOf)return array.indexOf(item, isSorted);
        for (; i < l; i++)if (array[i] === item)return i;
        return-1;
    };
    _.lastIndexOf = function (array, item, from) {
        if (array == null)return-1;
        var hasIndex = from != null;
        if (nativeLastIndexOf && array.lastIndexOf === nativeLastIndexOf) {
            return hasIndex ? array.lastIndexOf(item, from) : array.lastIndexOf(item);
        }
        var i = (hasIndex ? from : array.length);
        while (i--)if (array[i] === item)return i;
        return-1;
    };
    _.range = function (start, stop, step) {
        if (arguments.length <= 1) {
            stop = start || 0;
            start = 0;
        }
        step = arguments[2] || 1;
        var len = Math.max(Math.ceil((stop - start) / step), 0);
        var idx = 0;
        var range = new Array(len);
        while (idx < len) {
            range[idx++] = start;
            start += step;
        }
        return range;
    };
    _.bind = function (func, context) {
        if (func.bind === nativeBind && nativeBind)return nativeBind.apply(func, slice.call(arguments, 1));
        var args = slice.call(arguments, 2);
        return function () {
            return func.apply(context, args.concat(slice.call(arguments)));
        };
    };
    _.partial = function (func) {
        var args = slice.call(arguments, 1);
        return function () {
            return func.apply(this, args.concat(slice.call(arguments)));
        };
    };
    _.bindAll = function (obj) {
        var funcs = slice.call(arguments, 1);
        if (funcs.length === 0)funcs = _.functions(obj);
        each(funcs, function (f) {
            obj[f] = _.bind(obj[f], obj);
        });
        return obj;
    };
    _.memoize = function (func, hasher) {
        var memo = {};
        hasher || (hasher = _.identity);
        return function () {
            var key = hasher.apply(this, arguments);
            return _.has(memo, key) ? memo[key] : (memo[key] = func.apply(this, arguments));
        };
    };
    _.delay = function (func, wait) {
        var args = slice.call(arguments, 2);
        return setTimeout(function () {
            return func.apply(null, args);
        }, wait);
    };
    _.defer = function (func) {
        return _.delay.apply(_, [func, 1].concat(slice.call(arguments, 1)));
    };
    _.throttle = function (func, wait) {
        var context, args, timeout, result;
        var previous = 0;
        var later = function () {
            previous = new Date;
            timeout = null;
            result = func.apply(context, args);
        };
        return function () {
            var now = new Date;
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
            if (remaining <= 0) {
                clearTimeout(timeout);
                timeout = null;
                previous = now;
                result = func.apply(context, args);
            } else if (!timeout) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
    };
    _.debounce = function (func, wait, immediate) {
        var timeout, result;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate)result = func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow)result = func.apply(context, args);
            return result;
        };
    };
    _.once = function (func) {
        var ran = false, memo;
        return function () {
            if (ran)return memo;
            ran = true;
            memo = func.apply(this, arguments);
            func = null;
            return memo;
        };
    };
    _.wrap = function (func, wrapper) {
        return function () {
            var args = [func];
            push.apply(args, arguments);
            return wrapper.apply(this, args);
        };
    };
    _.compose = function () {
        var funcs = arguments;
        return function () {
            var args = arguments;
            for (var i = funcs.length - 1; i >= 0; i--) {
                args = [funcs[i].apply(this, args)];
            }
            return args[0];
        };
    };
    _.after = function (times, func) {
        if (times <= 0)return func();
        return function () {
            if (--times < 1) {
                return func.apply(this, arguments);
            }
        };
    };
    _.keys = nativeKeys || function (obj) {
        if (obj !== Object(obj))throw new TypeError('Invalid object');
        var keys = [];
        for (var key in obj)if (_.has(obj, key))keys[keys.length] = key;
        return keys;
    };
    _.values = function (obj) {
        var values = [];
        for (var key in obj)if (_.has(obj, key))values.push(obj[key]);
        return values;
    };
    _.pairs = function (obj) {
        var pairs = [];
        for (var key in obj)if (_.has(obj, key))pairs.push([key, obj[key]]);
        return pairs;
    };
    _.invert = function (obj) {
        var result = {};
        for (var key in obj)if (_.has(obj, key))result[obj[key]] = key;
        return result;
    };
    _.functions = _.methods = function (obj) {
        var names = [];
        for (var key in obj) {
            if (_.isFunction(obj[key]))names.push(key);
        }
        return names.sort();
    };
    _.extend = function (obj) {
        each(slice.call(arguments, 1), function (source) {
            if (source) {
                for (var prop in source) {
                    obj[prop] = source[prop];
                }
            }
        });
        return obj;
    };
    _.pick = function (obj) {
        var copy = {};
        var keys = concat.apply(ArrayProto, slice.call(arguments, 1));
        each(keys, function (key) {
            if (key in obj)copy[key] = obj[key];
        });
        return copy;
    };
    _.omit = function (obj) {
        var copy = {};
        var keys = concat.apply(ArrayProto, slice.call(arguments, 1));
        for (var key in obj) {
            if (!_.contains(keys, key))copy[key] = obj[key];
        }
        return copy;
    };
    _.defaults = function (obj) {
        each(slice.call(arguments, 1), function (source) {
            if (source) {
                for (var prop in source) {
                    if (obj[prop] == null)obj[prop] = source[prop];
                }
            }
        });
        return obj;
    };
    _.clone = function (obj) {
        if (!_.isObject(obj))return obj;
        return _.isArray(obj) ? obj.slice() : _.extend({}, obj);
    };
    _.tap = function (obj, interceptor) {
        interceptor(obj);
        return obj;
    };
    var eq = function (a, b, aStack, bStack) {
        if (a === b)return a !== 0 || 1 / a == 1 / b;
        if (a == null || b == null)return a === b;
        if (a instanceof _)a = a._wrapped;
        if (b instanceof _)b = b._wrapped;
        var className = toString.call(a);
        if (className != toString.call(b))return false;
        switch (className) {
            case'[object String]':
                return a == String(b);
            case'[object Number]':
                return a != +a ? b != +b : (a == 0 ? 1 / a == 1 / b : a == +b);
            case'[object Date]':
            case'[object Boolean]':
                return+a == +b;
            case'[object RegExp]':
                return a.source == b.source && a.global == b.global && a.multiline == b.multiline && a.ignoreCase == b.ignoreCase;
        }
        if (typeof a != 'object' || typeof b != 'object')return false;
        var length = aStack.length;
        while (length--) {
            if (aStack[length] == a)return bStack[length] == b;
        }
        aStack.push(a);
        bStack.push(b);
        var size = 0, result = true;
        if (className == '[object Array]') {
            size = a.length;
            result = size == b.length;
            if (result) {
                while (size--) {
                    if (!(result = eq(a[size], b[size], aStack, bStack)))break;
                }
            }
        } else {
            var aCtor = a.constructor, bCtor = b.constructor;
            if (aCtor !== bCtor && !(_.isFunction(aCtor) && (aCtor instanceof aCtor) && _.isFunction(bCtor) && (bCtor instanceof bCtor))) {
                return false;
            }
            for (var key in a) {
                if (_.has(a, key)) {
                    size++;
                    if (!(result = _.has(b, key) && eq(a[key], b[key], aStack, bStack)))break;
                }
            }
            if (result) {
                for (key in b) {
                    if (_.has(b, key) && !(size--))break;
                }
                result = !size;
            }
        }
        aStack.pop();
        bStack.pop();
        return result;
    };
    _.isEqual = function (a, b) {
        return eq(a, b, [], []);
    };
    _.isEmpty = function (obj) {
        if (obj == null)return true;
        if (_.isArray(obj) || _.isString(obj))return obj.length === 0;
        for (var key in obj)if (_.has(obj, key))return false;
        return true;
    };
    _.isElement = function (obj) {
        return!!(obj && obj.nodeType === 1);
    };
    _.isArray = nativeIsArray || function (obj) {
        return toString.call(obj) == '[object Array]';
    };
    _.isObject = function (obj) {
        return obj === Object(obj);
    };
    each(['Arguments', 'Function', 'String', 'Number', 'Date', 'RegExp'], function (name) {
        _['is' + name] = function (obj) {
            return toString.call(obj) == '[object ' + name + ']';
        };
    });
    if (!_.isArguments(arguments)) {
        _.isArguments = function (obj) {
            return!!(obj && _.has(obj, 'callee'));
        };
    }
    if (typeof(/./) !== 'function') {
        _.isFunction = function (obj) {
            return typeof obj === 'function';
        };
    }
    _.isFinite = function (obj) {
        return isFinite(obj) && !isNaN(parseFloat(obj));
    };
    _.isNaN = function (obj) {
        return _.isNumber(obj) && obj != +obj;
    };
    _.isBoolean = function (obj) {
        return obj === true || obj === false || toString.call(obj) == '[object Boolean]';
    };
    _.isNull = function (obj) {
        return obj === null;
    };
    _.isUndefined = function (obj) {
        return obj === void 0;
    };
    _.has = function (obj, key) {
        return hasOwnProperty.call(obj, key);
    };
    _.noConflict = function () {
        root._ = previousUnderscore;
        return this;
    };
    _.identity = function (value) {
        return value;
    };
    _.times = function (n, iterator, context) {
        var accum = Array(n);
        for (var i = 0; i < n; i++)accum[i] = iterator.call(context, i);
        return accum;
    };
    _.random = function (min, max) {
        if (max == null) {
            max = min;
            min = 0;
        }
        return min + Math.floor(Math.random() * (max - min + 1));
    };
    var entityMap = {escape: {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;', '/': '&#x2F;'}};
    entityMap.unescape = _.invert(entityMap.escape);
    var entityRegexes = {escape: new RegExp('[' + _.keys(entityMap.escape).join('') + ']', 'g'), unescape: new RegExp('(' + _.keys(entityMap.unescape).join('|') + ')', 'g')};
    _.each(['escape', 'unescape'], function (method) {
        _[method] = function (string) {
            if (string == null)return'';
            return('' + string).replace(entityRegexes[method], function (match) {
                return entityMap[method][match];
            });
        };
    });
    _.result = function (object, property) {
        if (object == null)return null;
        var value = object[property];
        return _.isFunction(value) ? value.call(object) : value;
    };
    _.mixin = function (obj) {
        each(_.functions(obj), function (name) {
            var func = _[name] = obj[name];
            _.prototype[name] = function () {
                var args = [this._wrapped];
                push.apply(args, arguments);
                return result.call(this, func.apply(_, args));
            };
        });
    };
    var idCounter = 0;
    _.uniqueId = function (prefix) {
        var id = ++idCounter + '';
        return prefix ? prefix + id : id;
    };
    _.templateSettings = {evaluate: /<%([\s\S]+?)%>/g, interpolate: /<%=([\s\S]+?)%>/g, escape: /<%-([\s\S]+?)%>/g};
    var noMatch = /(.)^/;
    var escapes = {"'": "'", '\\': '\\', '\r': 'r', '\n': 'n', '\t': 't', '\u2028': 'u2028', '\u2029': 'u2029'};
    var escaper = /\\|'|\r|\n|\t|\u2028|\u2029/g;
    _.template = function (text, data, settings) {
        var render;
        settings = _.defaults({}, settings, _.templateSettings);
        var matcher = new RegExp([(settings.escape || noMatch).source, (settings.interpolate || noMatch).source, (settings.evaluate || noMatch).source].join('|') + '|$', 'g');
        var index = 0;
        var source = "__p+='";
        text.replace(matcher, function (match, escape, interpolate, evaluate, offset) {
            source += text.slice(index, offset).replace(escaper, function (match) {
                return'\\' + escapes[match];
            });
            if (escape) {
                source += "'+\n((__t=(" + escape + "))==null?'':_.escape(__t))+\n'";
            }
            if (interpolate) {
                source += "'+\n((__t=(" + interpolate + "))==null?'':__t)+\n'";
            }
            if (evaluate) {
                source += "';\n" + evaluate + "\n__p+='";
            }
            index = offset + match.length;
            return match;
        });
        source += "';\n";
        if (!settings.variable)source = 'with(obj||{}){\n' + source + '}\n';
        source = "var __t,__p='',__j=Array.prototype.join," + "print=function(){__p+=__j.call(arguments,'');};\n" +
            source + "return __p;\n";
        try {
            render = new Function(settings.variable || 'obj', '_', source);
        } catch (e) {
            e.source = source;
            throw e;
        }
        if (data)return render(data, _);
        var template = function (data) {
            return render.call(this, data, _);
        };
        template.source = 'function(' + (settings.variable || 'obj') + '){\n' + source + '}';
        return template;
    };
    _.chain = function (obj) {
        return _(obj).chain();
    };
    var result = function (obj) {
        return this._chain ? _(obj).chain() : obj;
    };
    _.mixin(_);
    each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function (name) {
        var method = ArrayProto[name];
        _.prototype[name] = function () {
            var obj = this._wrapped;
            method.apply(obj, arguments);
            if ((name == 'shift' || name == 'splice') && obj.length === 0)delete obj[0];
            return result.call(this, obj);
        };
    });
    each(['concat', 'join', 'slice'], function (name) {
        var method = ArrayProto[name];
        _.prototype[name] = function () {
            return result.call(this, method.apply(this._wrapped, arguments));
        };
    });
    _.extend(_.prototype, {chain: function () {
        this._chain = true;
        return this;
    }, value: function () {
        return this._wrapped;
    }});
}).call(this);
(function () {
    var root = this;
    var previousBackbone = root.Backbone;
    var array = [];
    var push = array.push;
    var slice = array.slice;
    var splice = array.splice;
    var Backbone;
    if (typeof exports !== 'undefined') {
        Backbone = exports;
    } else {
        Backbone = root.Backbone = {};
    }
    Backbone.VERSION = '1.0.0';
    var _ = root._;
    if (!_ && (typeof require !== 'undefined'))_ = require('underscore');
    Backbone.$ = root.jQuery || root.Zepto || root.ender || root.$;
    Backbone.noConflict = function () {
        root.Backbone = previousBackbone;
        return this;
    };
    Backbone.emulateHTTP = false;
    Backbone.emulateJSON = false;
    var Events = Backbone.Events = {on: function (name, callback, context) {
        if (!eventsApi(this, 'on', name, [callback, context]) || !callback)return this;
        this._events || (this._events = {});
        var events = this._events[name] || (this._events[name] = []);
        events.push({callback: callback, context: context, ctx: context || this});
        return this;
    }, once: function (name, callback, context) {
        if (!eventsApi(this, 'once', name, [callback, context]) || !callback)return this;
        var self = this;
        var once = _.once(function () {
            self.off(name, once);
            callback.apply(this, arguments);
        });
        once._callback = callback;
        return this.on(name, once, context);
    }, off: function (name, callback, context) {
        var retain, ev, events, names, i, l, j, k;
        if (!this._events || !eventsApi(this, 'off', name, [callback, context]))return this;
        if (!name && !callback && !context) {
            this._events = {};
            return this;
        }
        names = name ? [name] : _.keys(this._events);
        for (i = 0, l = names.length; i < l; i++) {
            name = names[i];
            if (events = this._events[name]) {
                this._events[name] = retain = [];
                if (callback || context) {
                    for (j = 0, k = events.length; j < k; j++) {
                        ev = events[j];
                        if ((callback && callback !== ev.callback && callback !== ev.callback._callback) || (context && context !== ev.context)) {
                            retain.push(ev);
                        }
                    }
                }
                if (!retain.length)delete this._events[name];
            }
        }
        return this;
    }, trigger: function (name) {
        if (!this._events)return this;
        var args = slice.call(arguments, 1);
        if (!eventsApi(this, 'trigger', name, args))return this;
        var events = this._events[name];
        var allEvents = this._events.all;
        if (events)triggerEvents(events, args);
        if (allEvents)triggerEvents(allEvents, arguments);
        return this;
    }, stopListening: function (obj, name, callback) {
        var listeners = this._listeners;
        if (!listeners)return this;
        var deleteListener = !name && !callback;
        if (typeof name === 'object')callback = this;
        if (obj)(listeners = {})[obj._listenerId] = obj;
        for (var id in listeners) {
            listeners[id].off(name, callback, this);
            if (deleteListener)delete this._listeners[id];
        }
        return this;
    }};
    var eventSplitter = /\s+/;
    var eventsApi = function (obj, action, name, rest) {
        if (!name)return true;
        if (typeof name === 'object') {
            for (var key in name) {
                obj[action].apply(obj, [key, name[key]].concat(rest));
            }
            return false;
        }
        if (eventSplitter.test(name)) {
            var names = name.split(eventSplitter);
            for (var i = 0, l = names.length; i < l; i++) {
                obj[action].apply(obj, [names[i]].concat(rest));
            }
            return false;
        }
        return true;
    };
    var triggerEvents = function (events, args) {
        var ev, i = -1, l = events.length, a1 = args[0], a2 = args[1], a3 = args[2];
        switch (args.length) {
            case 0:
                while (++i < l)(ev = events[i]).callback.call(ev.ctx);
                return;
            case 1:
                while (++i < l)(ev = events[i]).callback.call(ev.ctx, a1);
                return;
            case 2:
                while (++i < l)(ev = events[i]).callback.call(ev.ctx, a1, a2);
                return;
            case 3:
                while (++i < l)(ev = events[i]).callback.call(ev.ctx, a1, a2, a3);
                return;
            default:
                while (++i < l)(ev = events[i]).callback.apply(ev.ctx, args);
        }
    };
    var listenMethods = {listenTo: 'on', listenToOnce: 'once'};
    _.each(listenMethods, function (implementation, method) {
        Events[method] = function (obj, name, callback) {
            var listeners = this._listeners || (this._listeners = {});
            var id = obj._listenerId || (obj._listenerId = _.uniqueId('l'));
            listeners[id] = obj;
            if (typeof name === 'object')callback = this;
            obj[implementation](name, callback, this);
            return this;
        };
    });
    Events.bind = Events.on;
    Events.unbind = Events.off;
    _.extend(Backbone, Events);
    var Model = Backbone.Model = function (attributes, options) {
        var defaults;
        var attrs = attributes || {};
        options || (options = {});
        this.cid = _.uniqueId('c');
        this.attributes = {};
        _.extend(this, _.pick(options, modelOptions));
        if (options.parse)attrs = this.parse(attrs, options) || {};
        if (defaults = _.result(this, 'defaults')) {
            attrs = _.defaults({}, attrs, defaults);
        }
        this.set(attrs, options);
        this.changed = {};
        this.initialize.apply(this, arguments);
    };
    var modelOptions = ['url', 'urlRoot', 'collection'];
    _.extend(Model.prototype, Events, {changed: null, validationError: null, idAttribute: 'id', initialize: function () {
    }, toJSON: function (options) {
        return _.clone(this.attributes);
    }, sync: function () {
        return Backbone.sync.apply(this, arguments);
    }, get: function (attr) {
        return this.attributes[attr];
    }, escape: function (attr) {
        return _.escape(this.get(attr));
    }, has: function (attr) {
        return this.get(attr) != null;
    }, set: function (key, val, options) {
        var attr, attrs, unset, changes, silent, changing, prev, current;
        if (key == null)return this;
        if (typeof key === 'object') {
            attrs = key;
            options = val;
        } else {
            (attrs = {})[key] = val;
        }
        options || (options = {});
        if (!this._validate(attrs, options))return false;
        unset = options.unset;
        silent = options.silent;
        changes = [];
        changing = this._changing;
        this._changing = true;
        if (!changing) {
            this._previousAttributes = _.clone(this.attributes);
            this.changed = {};
        }
        current = this.attributes, prev = this._previousAttributes;
        if (this.idAttribute in attrs)this.id = attrs[this.idAttribute];
        for (attr in attrs) {
            val = attrs[attr];
            if (!_.isEqual(current[attr], val))changes.push(attr);
            if (!_.isEqual(prev[attr], val)) {
                this.changed[attr] = val;
            } else {
                delete this.changed[attr];
            }
            unset ? delete current[attr] : current[attr] = val;
        }
        if (!silent) {
            if (changes.length)this._pending = true;
            for (var i = 0, l = changes.length; i < l; i++) {
                this.trigger('change:' + changes[i], this, current[changes[i]], options);
            }
        }
        if (changing)return this;
        if (!silent) {
            while (this._pending) {
                this._pending = false;
                this.trigger('change', this, options);
            }
        }
        this._pending = false;
        this._changing = false;
        return this;
    }, unset: function (attr, options) {
        return this.set(attr, void 0, _.extend({}, options, {unset: true}));
    }, clear: function (options) {
        var attrs = {};
        for (var key in this.attributes)attrs[key] = void 0;
        return this.set(attrs, _.extend({}, options, {unset: true}));
    }, hasChanged: function (attr) {
        if (attr == null)return!_.isEmpty(this.changed);
        return _.has(this.changed, attr);
    }, changedAttributes: function (diff) {
        if (!diff)return this.hasChanged() ? _.clone(this.changed) : false;
        var val, changed = false;
        var old = this._changing ? this._previousAttributes : this.attributes;
        for (var attr in diff) {
            if (_.isEqual(old[attr], (val = diff[attr])))continue;
            (changed || (changed = {}))[attr] = val;
        }
        return changed;
    }, previous: function (attr) {
        if (attr == null || !this._previousAttributes)return null;
        return this._previousAttributes[attr];
    }, previousAttributes: function () {
        return _.clone(this._previousAttributes);
    }, fetch: function (options) {
        options = options ? _.clone(options) : {};
        if (options.parse === void 0)options.parse = true;
        var model = this;
        var success = options.success;
        options.success = function (resp) {
            if (!model.set(model.parse(resp, options), options))return false;
            if (success)success(model, resp, options);
            model.trigger('sync', model, resp, options);
        };
        wrapError(this, options);
        return this.sync('read', this, options);
    }, save: function (key, val, options) {
        var attrs, method, xhr, attributes = this.attributes;
        if (key == null || typeof key === 'object') {
            attrs = key;
            options = val;
        } else {
            (attrs = {})[key] = val;
        }
        if (attrs && (!options || !options.wait) && !this.set(attrs, options))return false;
        options = _.extend({validate: true}, options);
        if (!this._validate(attrs, options))return false;
        if (attrs && options.wait) {
            this.attributes = _.extend({}, attributes, attrs);
        }
        if (options.parse === void 0)options.parse = true;
        var model = this;
        var success = options.success;
        options.success = function (resp) {
            model.attributes = attributes;
            var serverAttrs = model.parse(resp, options);
            if (options.wait)serverAttrs = _.extend(attrs || {}, serverAttrs);
            if (_.isObject(serverAttrs) && !model.set(serverAttrs, options)) {
                return false;
            }
            if (success)success(model, resp, options);
            model.trigger('sync', model, resp, options);
        };
        wrapError(this, options);
        method = this.isNew() ? 'create' : (options.patch ? 'patch' : 'update');
        if (method === 'patch')options.attrs = attrs;
        xhr = this.sync(method, this, options);
        if (attrs && options.wait)this.attributes = attributes;
        return xhr;
    }, destroy: function (options) {
        options = options ? _.clone(options) : {};
        var model = this;
        var success = options.success;
        var destroy = function () {
            model.trigger('destroy', model, model.collection, options);
        };
        options.success = function (resp) {
            if (options.wait || model.isNew())destroy();
            if (success)success(model, resp, options);
            if (!model.isNew())model.trigger('sync', model, resp, options);
        };
        if (this.isNew()) {
            options.success();
            return false;
        }
        wrapError(this, options);
        var xhr = this.sync('delete', this, options);
        if (!options.wait)destroy();
        return xhr;
    }, url: function () {
        var base = _.result(this, 'urlRoot') || _.result(this.collection, 'url') || urlError();
        if (this.isNew())return base;
        return base + (base.charAt(base.length - 1) === '/' ? '' : '/') + encodeURIComponent(this.id);
    }, parse: function (resp, options) {
        return resp;
    }, clone: function () {
        return new this.constructor(this.attributes);
    }, isNew: function () {
        return this.id == null;
    }, isValid: function (options) {
        return this._validate({}, _.extend(options || {}, {validate: true}));
    }, _validate: function (attrs, options) {
        if (!options.validate || !this.validate)return true;
        attrs = _.extend({}, this.attributes, attrs);
        var error = this.validationError = this.validate(attrs, options) || null;
        if (!error)return true;
        this.trigger('invalid', this, error, _.extend(options || {}, {validationError: error}));
        return false;
    }});
    var modelMethods = ['keys', 'values', 'pairs', 'invert', 'pick', 'omit'];
    _.each(modelMethods, function (method) {
        Model.prototype[method] = function () {
            var args = slice.call(arguments);
            args.unshift(this.attributes);
            return _[method].apply(_, args);
        };
    });
    var Collection = Backbone.Collection = function (models, options) {
        options || (options = {});
        if (options.url)this.url = options.url;
        if (options.model)this.model = options.model;
        if (options.comparator !== void 0)this.comparator = options.comparator;
        this._reset();
        this.initialize.apply(this, arguments);
        if (models)this.reset(models, _.extend({silent: true}, options));
    };
    var setOptions = {add: true, remove: true, merge: true};
    var addOptions = {add: true, merge: false, remove: false};
    _.extend(Collection.prototype, Events, {model: Model, initialize: function () {
    }, toJSON: function (options) {
        return this.map(function (model) {
            return model.toJSON(options);
        });
    }, sync: function () {
        return Backbone.sync.apply(this, arguments);
    }, add: function (models, options) {
        return this.set(models, _.defaults(options || {}, addOptions));
    }, remove: function (models, options) {
        models = _.isArray(models) ? models.slice() : [models];
        options || (options = {});
        var i, l, index, model;
        for (i = 0, l = models.length; i < l; i++) {
            model = this.get(models[i]);
            if (!model)continue;
            delete this._byId[model.id];
            delete this._byId[model.cid];
            index = this.indexOf(model);
            this.models.splice(index, 1);
            this.length--;
            if (!options.silent) {
                options.index = index;
                model.trigger('remove', model, this, options);
            }
            this._removeReference(model);
        }
        return this;
    }, set: function (models, options) {
        options = _.defaults(options || {}, setOptions);
        if (options.parse)models = this.parse(models, options);
        if (!_.isArray(models))models = models ? [models] : [];
        var i, l, model, attrs, existing, sort;
        var at = options.at;
        var sortable = this.comparator && (at == null) && options.sort !== false;
        var sortAttr = _.isString(this.comparator) ? this.comparator : null;
        var toAdd = [], toRemove = [], modelMap = {};
        for (i = 0, l = models.length; i < l; i++) {
            if (!(model = this._prepareModel(models[i], options)))continue;
            if (existing = this.get(model)) {
                if (options.remove)modelMap[existing.cid] = true;
                if (options.merge) {
                    existing.set(model.attributes, options);
                    if (sortable && !sort && existing.hasChanged(sortAttr))sort = true;
                }
            } else if (options.add) {
                toAdd.push(model);
                model.on('all', this._onModelEvent, this);
                this._byId[model.cid] = model;
                if (model.id != null)this._byId[model.id] = model;
            }
        }
        if (options.remove) {
            for (i = 0, l = this.length; i < l; ++i) {
                if (!modelMap[(model = this.models[i]).cid])toRemove.push(model);
            }
            if (toRemove.length)this.remove(toRemove, options);
        }
        if (toAdd.length) {
            if (sortable)sort = true;
            this.length += toAdd.length;
            if (at != null) {
                splice.apply(this.models, [at, 0].concat(toAdd));
            } else {
                push.apply(this.models, toAdd);
            }
        }
        if (sort)this.sort({silent: true});
        if (options.silent)return this;
        for (i = 0, l = toAdd.length; i < l; i++) {
            (model = toAdd[i]).trigger('add', model, this, options);
        }
        if (sort)this.trigger('sort', this, options);
        return this;
    }, reset: function (models, options) {
        options || (options = {});
        for (var i = 0, l = this.models.length; i < l; i++) {
            this._removeReference(this.models[i]);
        }
        options.previousModels = this.models;
        this._reset();
        this.add(models, _.extend({silent: true}, options));
        if (!options.silent)this.trigger('reset', this, options);
        return this;
    }, push: function (model, options) {
        model = this._prepareModel(model, options);
        this.add(model, _.extend({at: this.length}, options));
        return model;
    }, pop: function (options) {
        var model = this.at(this.length - 1);
        this.remove(model, options);
        return model;
    }, unshift: function (model, options) {
        model = this._prepareModel(model, options);
        this.add(model, _.extend({at: 0}, options));
        return model;
    }, shift: function (options) {
        var model = this.at(0);
        this.remove(model, options);
        return model;
    }, slice: function (begin, end) {
        return this.models.slice(begin, end);
    }, get: function (obj) {
        if (obj == null)return void 0;
        return this._byId[obj.id != null ? obj.id : obj.cid || obj];
    }, at: function (index) {
        return this.models[index];
    }, where: function (attrs, first) {
        if (_.isEmpty(attrs))return first ? void 0 : [];
        return this[first ? 'find' : 'filter'](function (model) {
            for (var key in attrs) {
                if (attrs[key] !== model.get(key))return false;
            }
            return true;
        });
    }, findWhere: function (attrs) {
        return this.where(attrs, true);
    }, sort: function (options) {
        if (!this.comparator)throw new Error('Cannot sort a set without a comparator');
        options || (options = {});
        if (_.isString(this.comparator) || this.comparator.length === 1) {
            this.models = this.sortBy(this.comparator, this);
        } else {
            this.models.sort(_.bind(this.comparator, this));
        }
        if (!options.silent)this.trigger('sort', this, options);
        return this;
    }, sortedIndex: function (model, value, context) {
        value || (value = this.comparator);
        var iterator = _.isFunction(value) ? value : function (model) {
            return model.get(value);
        };
        return _.sortedIndex(this.models, model, iterator, context);
    }, pluck: function (attr) {
        return _.invoke(this.models, 'get', attr);
    }, fetch: function (options) {
        options = options ? _.clone(options) : {};
        if (options.parse === void 0)options.parse = true;
        var success = options.success;
        var collection = this;
        options.success = function (resp) {
            var method = options.reset ? 'reset' : 'set';
            collection[method](resp, options);
            if (success)success(collection, resp, options);
            collection.trigger('sync', collection, resp, options);
        };
        wrapError(this, options);
        return this.sync('read', this, options);
    }, create: function (model, options) {
        options = options ? _.clone(options) : {};
        if (!(model = this._prepareModel(model, options)))return false;
        if (!options.wait)this.add(model, options);
        var collection = this;
        var success = options.success;
        options.success = function (resp) {
            if (options.wait)collection.add(model, options);
            if (success)success(model, resp, options);
        };
        model.save(null, options);
        return model;
    }, parse: function (resp, options) {
        return resp;
    }, clone: function () {
        return new this.constructor(this.models);
    }, _reset: function () {
        this.length = 0;
        this.models = [];
        this._byId = {};
    }, _prepareModel: function (attrs, options) {
        if (attrs instanceof Model) {
            if (!attrs.collection)attrs.collection = this;
            return attrs;
        }
        options || (options = {});
        options.collection = this;
        var model = new this.model(attrs, options);
        if (!model._validate(attrs, options)) {
            this.trigger('invalid', this, attrs, options);
            return false;
        }
        return model;
    }, _removeReference: function (model) {
        if (this === model.collection)delete model.collection;
        model.off('all', this._onModelEvent, this);
    }, _onModelEvent: function (event, model, collection, options) {
        if ((event === 'add' || event === 'remove') && collection !== this)return;
        if (event === 'destroy')this.remove(model, options);
        if (model && event === 'change:' + model.idAttribute) {
            delete this._byId[model.previous(model.idAttribute)];
            if (model.id != null)this._byId[model.id] = model;
        }
        this.trigger.apply(this, arguments);
    }});
    var methods = ['forEach', 'each', 'map', 'collect', 'reduce', 'foldl', 'inject', 'reduceRight', 'foldr', 'find', 'detect', 'filter', 'select', 'reject', 'every', 'all', 'some', 'any', 'include', 'contains', 'invoke', 'max', 'min', 'toArray', 'size', 'first', 'head', 'take', 'initial', 'rest', 'tail', 'drop', 'last', 'without', 'indexOf', 'shuffle', 'lastIndexOf', 'isEmpty', 'chain'];
    _.each(methods, function (method) {
        Collection.prototype[method] = function () {
            var args = slice.call(arguments);
            args.unshift(this.models);
            return _[method].apply(_, args);
        };
    });
    var attributeMethods = ['groupBy', 'countBy', 'sortBy'];
    _.each(attributeMethods, function (method) {
        Collection.prototype[method] = function (value, context) {
            var iterator = _.isFunction(value) ? value : function (model) {
                return model.get(value);
            };
            return _[method](this.models, iterator, context);
        };
    });
    var View = Backbone.View = function (options) {
        this.cid = _.uniqueId('view');
        this._configure(options || {});
        this._ensureElement();
        this.initialize.apply(this, arguments);
        this.delegateEvents();
    };
    var delegateEventSplitter = /^(\S+)\s*(.*)$/;
    var viewOptions = ['model', 'collection', 'el', 'id', 'attributes', 'className', 'tagName', 'events'];
    _.extend(View.prototype, Events, {tagName: 'div', $: function (selector) {
        return this.$el.find(selector);
    }, initialize: function () {
    }, render: function () {
        return this;
    }, remove: function () {
        this.$el.remove();
        this.stopListening();
        return this;
    }, setElement: function (element, delegate) {
        if (this.$el)this.undelegateEvents();
        this.$el = element instanceof Backbone.$ ? element : Backbone.$(element);
        this.el = this.$el[0];
        if (delegate !== false)this.delegateEvents();
        return this;
    },
        delegateEvents: function (events) {
            if (!(events || (events = _.result(this, 'events'))))return this;
            this.undelegateEvents();
            for (var key in events) {
                var method = events[key];
                if (!_.isFunction(method))method = this[events[key]];
                if (!method)continue;
                var match = key.match(delegateEventSplitter);
                var eventName = match[1], selector = match[2];
                method = _.bind(method, this);
                eventName += '.delegateEvents' + this.cid;
                if (selector === '') {
                    this.$el.on(eventName, method);
                } else {
                    this.$el.on(eventName, selector, method);
                }
            }
            return this;
        }, undelegateEvents: function () {
            this.$el.off('.delegateEvents' + this.cid);
            return this;
        }, _configure: function (options) {
            if (this.options)options = _.extend({}, _.result(this, 'options'), options);
            _.extend(this, _.pick(options, viewOptions));
            this.options = options;
        }, _ensureElement: function () {
            if (!this.el) {
                var attrs = _.extend({}, _.result(this, 'attributes'));
                if (this.id)attrs.id = _.result(this, 'id');
                if (this.className)attrs['class'] = _.result(this, 'className');
                var $el = Backbone.$('<' + _.result(this, 'tagName') + '>').attr(attrs);
                this.setElement($el, false);
            } else {
                this.setElement(_.result(this, 'el'), false);
            }
        }});
    Backbone.sync = function (method, model, options) {
        var type = methodMap[method];
        _.defaults(options || (options = {}), {emulateHTTP: Backbone.emulateHTTP, emulateJSON: Backbone.emulateJSON});
        var params = {type: type, dataType: 'json'};
        if (!options.url) {
            params.url = _.result(model, 'url') || urlError();
        }
        if (options.data == null && model && (method === 'create' || method === 'update' || method === 'patch')) {
            params.contentType = 'application/json';
            params.data = JSON.stringify(options.attrs || model.toJSON(options));
        }
        if (options.emulateJSON) {
            params.contentType = 'application/x-www-form-urlencoded';
            params.data = params.data ? {model: params.data} : {};
        }
        if (options.emulateHTTP && (type === 'PUT' || type === 'DELETE' || type === 'PATCH')) {
            params.type = 'POST';
            if (options.emulateJSON)params.data._method = type;
            var beforeSend = options.beforeSend;
            options.beforeSend = function (xhr) {
                xhr.setRequestHeader('X-HTTP-Method-Override', type);
                if (beforeSend)return beforeSend.apply(this, arguments);
            };
        }
        if (params.type !== 'GET' && !options.emulateJSON) {
            params.processData = false;
        }
        if (params.type === 'PATCH' && window.ActiveXObject && !(window.external && window.external.msActiveXFilteringEnabled)) {
            params.xhr = function () {
                return new ActiveXObject("Microsoft.XMLHTTP");
            };
        }
        var xhr = options.xhr = Backbone.ajax(_.extend(params, options));
        model.trigger('request', model, xhr, options);
        return xhr;
    };
    var methodMap = {'create': 'POST', 'update': 'PUT', 'patch': 'PATCH', 'delete': 'DELETE', 'read': 'GET'};
    Backbone.ajax = function () {
        return Backbone.$.ajax.apply(Backbone.$, arguments);
    };
    var Router = Backbone.Router = function (options) {
        options || (options = {});
        if (options.routes)this.routes = options.routes;
        this._bindRoutes();
        this.initialize.apply(this, arguments);
    };
    var optionalParam = /\((.*?)\)/g;
    var namedParam = /(\(\?)?:\w+/g;
    var splatParam = /\*\w+/g;
    var escapeRegExp = /[\-{}\[\]+?.,\\\^$|#\s]/g;
    _.extend(Router.prototype, Events, {initialize: function () {
    }, route: function (route, name, callback) {
        if (!_.isRegExp(route))route = this._routeToRegExp(route);
        if (_.isFunction(name)) {
            callback = name;
            name = '';
        }
        if (!callback)callback = this[name];
        var router = this;
        Backbone.history.route(route, function (fragment) {
            var args = router._extractParameters(route, fragment);
            callback && callback.apply(router, args);
            router.trigger.apply(router, ['route:' + name].concat(args));
            router.trigger('route', name, args);
            Backbone.history.trigger('route', router, name, args);
        });
        return this;
    }, navigate: function (fragment, options) {
        Backbone.history.navigate(fragment, options);
        return this;
    }, _bindRoutes: function () {
        if (!this.routes)return;
        this.routes = _.result(this, 'routes');
        var route, routes = _.keys(this.routes);
        while ((route = routes.pop()) != null) {
            this.route(route, this.routes[route]);
        }
    }, _routeToRegExp: function (route) {
        route = route.replace(escapeRegExp, '\\$&').replace(optionalParam, '(?:$1)?').replace(namedParam,function (match, optional) {
            return optional ? match : '([^\/]+)';
        }).replace(splatParam, '(.*?)');
        return new RegExp('^' + route + '$');
    }, _extractParameters: function (route, fragment) {
        var params = route.exec(fragment).slice(1);
        return _.map(params, function (param) {
            return param ? decodeURIComponent(param) : null;
        });
    }});
    var History = Backbone.History = function () {
        this.handlers = [];
        _.bindAll(this, 'checkUrl');
        if (typeof window !== 'undefined') {
            this.location = window.location;
            this.history = window.history;
        }
    };
    var routeStripper = /^[#\/]|\s+$/g;
    var rootStripper = /^\/+|\/+$/g;
    var isExplorer = /msie [\w.]+/;
    var trailingSlash = /\/$/;
    History.started = false;
    _.extend(History.prototype, Events, {interval: 50, getHash: function (window) {
        var match = (window || this).location.href.match(/#(.*)$/);
        return match ? match[1] : '';
    }, getFragment: function (fragment, forcePushState) {
        if (fragment == null) {
            if (this._hasPushState || !this._wantsHashChange || forcePushState) {
                fragment = this.location.pathname;
                var root = this.root.replace(trailingSlash, '');
                if (!fragment.indexOf(root))fragment = fragment.substr(root.length);
            } else {
                fragment = this.getHash();
            }
        }
        return fragment.replace(routeStripper, '');
    }, start: function (options) {
        if (History.started)throw new Error("Backbone.history has already been started");
        History.started = true;
        this.options = _.extend({}, {root: '/'}, this.options, options);
        this.root = this.options.root;
        this._wantsHashChange = this.options.hashChange !== false;
        this._wantsPushState = !!this.options.pushState;
        this._hasPushState = !!(this.options.pushState && this.history && this.history.pushState);
        var fragment = this.getFragment();
        var docMode = document.documentMode;
        var oldIE = (isExplorer.exec(navigator.userAgent.toLowerCase()) && (!docMode || docMode <= 7));
        this.root = ('/' + this.root + '/').replace(rootStripper, '/');
        if (oldIE && this._wantsHashChange) {
            this.iframe = Backbone.$('<iframe src="javascript:0" tabindex="-1" />').hide().appendTo('body')[0].contentWindow;
            this.navigate(fragment);
        }
        if (this._hasPushState) {
            Backbone.$(window).on('popstate', this.checkUrl);
        } else if (this._wantsHashChange && ('onhashchange'in window) && !oldIE) {
            Backbone.$(window).on('hashchange', this.checkUrl);
        } else if (this._wantsHashChange) {
            this._checkUrlInterval = setInterval(this.checkUrl, this.interval);
        }
        this.fragment = fragment;
        var loc = this.location;
        var atRoot = loc.pathname.replace(/[^\/]$/, '$&/') === this.root;
        if (this._wantsHashChange && this._wantsPushState && !this._hasPushState && !atRoot) {
            this.fragment = this.getFragment(null, true);
            this.location.replace(this.root + this.location.search + '#' + this.fragment);
            return true;
        } else if (this._wantsPushState && this._hasPushState && atRoot && loc.hash) {
            this.fragment = this.getHash().replace(routeStripper, '');
            this.history.replaceState({}, document.title, this.root + this.fragment + loc.search);
        }
        if (!this.options.silent)return this.loadUrl();
    }, stop: function () {
        Backbone.$(window).off('popstate', this.checkUrl).off('hashchange', this.checkUrl);
        clearInterval(this._checkUrlInterval);
        History.started = false;
    }, route: function (route, callback) {
        this.handlers.unshift({route: route, callback: callback});
    }, checkUrl: function (e) {
        var current = this.getFragment();
        if (current === this.fragment && this.iframe) {
            current = this.getFragment(this.getHash(this.iframe));
        }
        if (current === this.fragment)return false;
        if (this.iframe)this.navigate(current);
        this.loadUrl() || this.loadUrl(this.getHash());
    }, loadUrl: function (fragmentOverride) {
        var fragment = this.fragment = this.getFragment(fragmentOverride);
        var matched = _.any(this.handlers, function (handler) {
            if (handler.route.test(fragment)) {
                handler.callback(fragment);
                return true;
            }
        });
        return matched;
    }, navigate: function (fragment, options) {
        if (!History.started)return false;
        if (!options || options === true)options = {trigger: options};
        fragment = this.getFragment(fragment || '');
        if (this.fragment === fragment)return;
        this.fragment = fragment;
        var url = this.root + fragment;
        if (this._hasPushState) {
            this.history[options.replace ? 'replaceState' : 'pushState']({}, document.title, url);
        } else if (this._wantsHashChange) {
            this._updateHash(this.location, fragment, options.replace);
            if (this.iframe && (fragment !== this.getFragment(this.getHash(this.iframe)))) {
                if (!options.replace)this.iframe.document.open().close();
                this._updateHash(this.iframe.location, fragment, options.replace);
            }
        } else {
            return this.location.assign(url);
        }
        if (options.trigger)this.loadUrl(fragment);
    }, _updateHash: function (location, fragment, replace) {
        if (replace) {
            var href = location.href.replace(/(javascript:|#).*$/, '');
            location.replace(href + '#' + fragment);
        } else {
            location.hash = '#' + fragment;
        }
    }});
    Backbone.history = new History;
    var extend = function (protoProps, staticProps) {
        var parent = this;
        var child;
        if (protoProps && _.has(protoProps, 'constructor')) {
            child = protoProps.constructor;
        } else {
            child = function () {
                return parent.apply(this, arguments);
            };
        }
        _.extend(child, parent, staticProps);
        var Surrogate = function () {
            this.constructor = child;
        };
        Surrogate.prototype = parent.prototype;
        child.prototype = new Surrogate;
        if (protoProps)_.extend(child.prototype, protoProps);
        child.__super__ = parent.prototype;
        return child;
    };
    Model.extend = Collection.extend = Router.extend = View.extend = History.extend = extend;
    var urlError = function () {
        throw new Error('A "url" property or function must be specified');
    };
    var wrapError = function (model, options) {
        var error = options.error;
        options.error = function (resp) {
            if (error)error(model, resp, options);
            model.trigger('error', model, resp, options);
        };
    };
}).call(this);
var Base64 = (function () {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var obj = {encode: function (input) {
        var output = "";
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        do {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);
            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;
            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }
            output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) +
                keyStr.charAt(enc3) + keyStr.charAt(enc4);
        } while (i < input.length);
        return output;
    }, decode: function (input) {
        var output = "";
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        do {
            enc1 = keyStr.indexOf(input.charAt(i++));
            enc2 = keyStr.indexOf(input.charAt(i++));
            enc3 = keyStr.indexOf(input.charAt(i++));
            enc4 = keyStr.indexOf(input.charAt(i++));
            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;
            output = output + String.fromCharCode(chr1);
            if (enc3 != 64) {
                output = output + String.fromCharCode(chr2);
            }
            if (enc4 != 64) {
                output = output + String.fromCharCode(chr3);
            }
        } while (i < input.length);
        return output;
    }};
    return obj;
})();
var MD5 = (function () {
    var hexcase = 0;
    var b64pad = "";
    var chrsz = 8;
    var safe_add = function (x, y) {
        var lsw = (x & 0xFFFF) + (y & 0xFFFF);
        var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
        return(msw << 16) | (lsw & 0xFFFF);
    };
    var bit_rol = function (num, cnt) {
        return(num << cnt) | (num >>> (32 - cnt));
    };
    var str2binl = function (str) {
        var bin = [];
        var mask = (1 << chrsz) - 1;
        for (var i = 0; i < str.length * chrsz; i += chrsz) {
            bin[i >> 5] |= (str.charCodeAt(i / chrsz) & mask) << (i % 32);
        }
        return bin;
    };
    var binl2str = function (bin) {
        var str = "";
        var mask = (1 << chrsz) - 1;
        for (var i = 0; i < bin.length * 32; i += chrsz) {
            str += String.fromCharCode((bin[i >> 5] >>> (i % 32)) & mask);
        }
        return str;
    };
    var binl2hex = function (binarray) {
        var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
        var str = "";
        for (var i = 0; i < binarray.length * 4; i++) {
            str += hex_tab.charAt((binarray[i >> 2] >> ((i % 4) * 8 + 4)) & 0xF) +
                hex_tab.charAt((binarray[i >> 2] >> ((i % 4) * 8)) & 0xF);
        }
        return str;
    };
    var binl2b64 = function (binarray) {
        var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        var str = "";
        var triplet, j;
        for (var i = 0; i < binarray.length * 4; i += 3) {
            triplet = (((binarray[i >> 2] >> 8 * (i % 4)) & 0xFF) << 16) | (((binarray[i + 1 >> 2] >> 8 * ((i + 1) % 4)) & 0xFF) << 8) | ((binarray[i + 2 >> 2] >> 8 * ((i + 2) % 4)) & 0xFF);
            for (j = 0; j < 4; j++) {
                if (i * 8 + j * 6 > binarray.length * 32) {
                    str += b64pad;
                }
                else {
                    str += tab.charAt((triplet >> 6 * (3 - j)) & 0x3F);
                }
            }
        }
        return str;
    };
    var md5_cmn = function (q, a, b, x, s, t) {
        return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b);
    };
    var md5_ff = function (a, b, c, d, x, s, t) {
        return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
    };
    var md5_gg = function (a, b, c, d, x, s, t) {
        return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
    };
    var md5_hh = function (a, b, c, d, x, s, t) {
        return md5_cmn(b ^ c ^ d, a, b, x, s, t);
    };
    var md5_ii = function (a, b, c, d, x, s, t) {
        return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
    };
    var core_md5 = function (x, len) {
        x[len >> 5] |= 0x80 << ((len) % 32);
        x[(((len + 64) >>> 9) << 4) + 14] = len;
        var a = 1732584193;
        var b = -271733879;
        var c = -1732584194;
        var d = 271733878;
        var olda, oldb, oldc, oldd;
        for (var i = 0; i < x.length; i += 16) {
            olda = a;
            oldb = b;
            oldc = c;
            oldd = d;
            a = md5_ff(a, b, c, d, x[i + 0], 7, -680876936);
            d = md5_ff(d, a, b, c, x[i + 1], 12, -389564586);
            c = md5_ff(c, d, a, b, x[i + 2], 17, 606105819);
            b = md5_ff(b, c, d, a, x[i + 3], 22, -1044525330);
            a = md5_ff(a, b, c, d, x[i + 4], 7, -176418897);
            d = md5_ff(d, a, b, c, x[i + 5], 12, 1200080426);
            c = md5_ff(c, d, a, b, x[i + 6], 17, -1473231341);
            b = md5_ff(b, c, d, a, x[i + 7], 22, -45705983);
            a = md5_ff(a, b, c, d, x[i + 8], 7, 1770035416);
            d = md5_ff(d, a, b, c, x[i + 9], 12, -1958414417);
            c = md5_ff(c, d, a, b, x[i + 10], 17, -42063);
            b = md5_ff(b, c, d, a, x[i + 11], 22, -1990404162);
            a = md5_ff(a, b, c, d, x[i + 12], 7, 1804603682);
            d = md5_ff(d, a, b, c, x[i + 13], 12, -40341101);
            c = md5_ff(c, d, a, b, x[i + 14], 17, -1502002290);
            b = md5_ff(b, c, d, a, x[i + 15], 22, 1236535329);
            a = md5_gg(a, b, c, d, x[i + 1], 5, -165796510);
            d = md5_gg(d, a, b, c, x[i + 6], 9, -1069501632);
            c = md5_gg(c, d, a, b, x[i + 11], 14, 643717713);
            b = md5_gg(b, c, d, a, x[i + 0], 20, -373897302);
            a = md5_gg(a, b, c, d, x[i + 5], 5, -701558691);
            d = md5_gg(d, a, b, c, x[i + 10], 9, 38016083);
            c = md5_gg(c, d, a, b, x[i + 15], 14, -660478335);
            b = md5_gg(b, c, d, a, x[i + 4], 20, -405537848);
            a = md5_gg(a, b, c, d, x[i + 9], 5, 568446438);
            d = md5_gg(d, a, b, c, x[i + 14], 9, -1019803690);
            c = md5_gg(c, d, a, b, x[i + 3], 14, -187363961);
            b = md5_gg(b, c, d, a, x[i + 8], 20, 1163531501);
            a = md5_gg(a, b, c, d, x[i + 13], 5, -1444681467);
            d = md5_gg(d, a, b, c, x[i + 2], 9, -51403784);
            c = md5_gg(c, d, a, b, x[i + 7], 14, 1735328473);
            b = md5_gg(b, c, d, a, x[i + 12], 20, -1926607734);
            a = md5_hh(a, b, c, d, x[i + 5], 4, -378558);
            d = md5_hh(d, a, b, c, x[i + 8], 11, -2022574463);
            c = md5_hh(c, d, a, b, x[i + 11], 16, 1839030562);
            b = md5_hh(b, c, d, a, x[i + 14], 23, -35309556);
            a = md5_hh(a, b, c, d, x[i + 1], 4, -1530992060);
            d = md5_hh(d, a, b, c, x[i + 4], 11, 1272893353);
            c = md5_hh(c, d, a, b, x[i + 7], 16, -155497632);
            b = md5_hh(b, c, d, a, x[i + 10], 23, -1094730640);
            a = md5_hh(a, b, c, d, x[i + 13], 4, 681279174);
            d = md5_hh(d, a, b, c, x[i + 0], 11, -358537222);
            c = md5_hh(c, d, a, b, x[i + 3], 16, -722521979);
            b = md5_hh(b, c, d, a, x[i + 6], 23, 76029189);
            a = md5_hh(a, b, c, d, x[i + 9], 4, -640364487);
            d = md5_hh(d, a, b, c, x[i + 12], 11, -421815835);
            c = md5_hh(c, d, a, b, x[i + 15], 16, 530742520);
            b = md5_hh(b, c, d, a, x[i + 2], 23, -995338651);
            a = md5_ii(a, b, c, d, x[i + 0], 6, -198630844);
            d = md5_ii(d, a, b, c, x[i + 7], 10, 1126891415);
            c = md5_ii(c, d, a, b, x[i + 14], 15, -1416354905);
            b = md5_ii(b, c, d, a, x[i + 5], 21, -57434055);
            a = md5_ii(a, b, c, d, x[i + 12], 6, 1700485571);
            d = md5_ii(d, a, b, c, x[i + 3], 10, -1894986606);
            c = md5_ii(c, d, a, b, x[i + 10], 15, -1051523);
            b = md5_ii(b, c, d, a, x[i + 1], 21, -2054922799);
            a = md5_ii(a, b, c, d, x[i + 8], 6, 1873313359);
            d = md5_ii(d, a, b, c, x[i + 15], 10, -30611744);
            c = md5_ii(c, d, a, b, x[i + 6], 15, -1560198380);
            b = md5_ii(b, c, d, a, x[i + 13], 21, 1309151649);
            a = md5_ii(a, b, c, d, x[i + 4], 6, -145523070);
            d = md5_ii(d, a, b, c, x[i + 11], 10, -1120210379);
            c = md5_ii(c, d, a, b, x[i + 2], 15, 718787259);
            b = md5_ii(b, c, d, a, x[i + 9], 21, -343485551);
            a = safe_add(a, olda);
            b = safe_add(b, oldb);
            c = safe_add(c, oldc);
            d = safe_add(d, oldd);
        }
        return[a, b, c, d];
    };
    var core_hmac_md5 = function (key, data) {
        var bkey = str2binl(key);
        if (bkey.length > 16) {
            bkey = core_md5(bkey, key.length * chrsz);
        }
        var ipad = new Array(16), opad = new Array(16);
        for (var i = 0; i < 16; i++) {
            ipad[i] = bkey[i] ^ 0x36363636;
            opad[i] = bkey[i] ^ 0x5C5C5C5C;
        }
        var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
        return core_md5(opad.concat(hash), 512 + 128);
    };
    var obj = {hexdigest: function (s) {
        return binl2hex(core_md5(str2binl(s), s.length * chrsz));
    }, b64digest: function (s) {
        return binl2b64(core_md5(str2binl(s), s.length * chrsz));
    }, hash: function (s) {
        return binl2str(core_md5(str2binl(s), s.length * chrsz));
    }, hmac_hexdigest: function (key, data) {
        return binl2hex(core_hmac_md5(key, data));
    }, hmac_b64digest: function (key, data) {
        return binl2b64(core_hmac_md5(key, data));
    }, hmac_hash: function (key, data) {
        return binl2str(core_hmac_md5(key, data));
    }, test: function () {
        return MD5.hexdigest("abc") === "900150983cd24fb0d6963f7d28e17f72";
    }};
    return obj;
})();
if (!Function.prototype.bind) {
    Function.prototype.bind = function (obj) {
        var func = this;
        var _slice = Array.prototype.slice;
        var _concat = Array.prototype.concat;
        var _args = _slice.call(arguments, 1);
        return function () {
            return func.apply(obj ? obj : this, _concat.call(_args, _slice.call(arguments, 0)));
        };
    };
}
if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function (elt) {
        var len = this.length;
        var from = Number(arguments[1]) || 0;
        from = (from < 0) ? Math.ceil(from) : Math.floor(from);
        if (from < 0) {
            from += len;
        }
        for (; from < len; from++) {
            if (from in this && this[from] === elt) {
                return from;
            }
        }
        return-1;
    };
}
(function (callback) {
    var Strophe;

    function $build(name, attrs) {
        return new Strophe.Builder(name, attrs);
    }

    function $msg(attrs) {
        return new Strophe.Builder("message", attrs);
    }

    function $iq(attrs) {
        return new Strophe.Builder("iq", attrs);
    }

    function $pres(attrs) {
        return new Strophe.Builder("presence", attrs);
    }

    Strophe = {VERSION: "1.0.2", NS: {HTTPBIND: "http://jabber.org/protocol/httpbind", BOSH: "urn:xmpp:xbosh", CLIENT: "jabber:client", AUTH: "jabber:iq:auth", ROSTER: "jabber:iq:roster", PROFILE: "jabber:iq:profile", DISCO_INFO: "http://jabber.org/protocol/disco#info", DISCO_ITEMS: "http://jabber.org/protocol/disco#items", MUC: "http://jabber.org/protocol/muc", SASL: "urn:ietf:params:xml:ns:xmpp-sasl", STREAM: "http://etherx.jabber.org/streams", BIND: "urn:ietf:params:xml:ns:xmpp-bind", SESSION: "urn:ietf:params:xml:ns:xmpp-session", VERSION: "jabber:iq:version", STANZAS: "urn:ietf:params:xml:ns:xmpp-stanzas"}, addNamespace: function (name, value) {
        Strophe.NS[name] = value;
    }, Status: {ERROR: 0, CONNECTING: 1, CONNFAIL: 2, AUTHENTICATING: 3, AUTHFAIL: 4, CONNECTED: 5, DISCONNECTED: 6, DISCONNECTING: 7, ATTACHED: 8}, LogLevel: {DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3, FATAL: 4}, ElementType: {NORMAL: 1, TEXT: 3, CDATA: 4}, TIMEOUT: 1.1, SECONDARY_TIMEOUT: 0.1, forEachChild: function (elem, elemName, func) {
        var i, childNode;
        for (i = 0; i < elem.childNodes.length; i++) {
            childNode = elem.childNodes[i];
            if (childNode.nodeType == Strophe.ElementType.NORMAL && (!elemName || this.isTagEqual(childNode, elemName))) {
                func(childNode);
            }
        }
    }, isTagEqual: function (el, name) {
        return el.tagName.toLowerCase() == name.toLowerCase();
    }, _xmlGenerator: null, _makeGenerator: function () {
        var doc;
        if (document.implementation.createDocument === undefined) {
            doc = this._getIEXmlDom();
            doc.appendChild(doc.createElement('strophe'));
        } else {
            doc = document.implementation.createDocument('jabber:client', 'strophe', null);
        }
        return doc;
    }, xmlGenerator: function () {
        if (!Strophe._xmlGenerator) {
            Strophe._xmlGenerator = Strophe._makeGenerator();
        }
        return Strophe._xmlGenerator;
    }, _getIEXmlDom: function () {
        var doc = null;
        var docStrings = ["Msxml2.DOMDocument.6.0", "Msxml2.DOMDocument.5.0", "Msxml2.DOMDocument.4.0", "MSXML2.DOMDocument.3.0", "MSXML2.DOMDocument", "MSXML.DOMDocument", "Microsoft.XMLDOM"];
        for (var d = 0; d < docStrings.length; d++) {
            if (doc === null) {
                try {
                    doc = new ActiveXObject(docStrings[d]);
                } catch (e) {
                    doc = null;
                }
            } else {
                break;
            }
        }
        return doc;
    }, xmlElement: function (name) {
        if (!name) {
            return null;
        }
        var node = Strophe.xmlGenerator().createElement(name);
        var a, i, k;
        for (a = 1; a < arguments.length; a++) {
            if (!arguments[a]) {
                continue;
            }
            if (typeof(arguments[a]) == "string" || typeof(arguments[a]) == "number") {
                node.appendChild(Strophe.xmlTextNode(arguments[a]));
            } else if (typeof(arguments[a]) == "object" && typeof(arguments[a].sort) == "function") {
                for (i = 0; i < arguments[a].length; i++) {
                    if (typeof(arguments[a][i]) == "object" && typeof(arguments[a][i].sort) == "function") {
                        node.setAttribute(arguments[a][i][0], arguments[a][i][1]);
                    }
                }
            } else if (typeof(arguments[a]) == "object") {
                for (k in arguments[a]) {
                    if (arguments[a].hasOwnProperty(k)) {
                        node.setAttribute(k, arguments[a][k]);
                    }
                }
            }
        }
        return node;
    }, xmlescape: function (text) {
        text = text.replace(/\&/g, "&amp;");
        text = text.replace(/</g, "&lt;");
        text = text.replace(/>/g, "&gt;");
        text = text.replace(/'/g, "&apos;");
        text = text.replace(/"/g, "&quot;");
        return text;
    }, xmlTextNode: function (text) {
        text = Strophe.xmlescape(text);
        return Strophe.xmlGenerator().createTextNode(text);
    }, getText: function (elem) {
        if (!elem) {
            return null;
        }
        var str = "";
        if (elem.childNodes.length === 0 && elem.nodeType == Strophe.ElementType.TEXT) {
            str += elem.nodeValue;
        }
        for (var i = 0; i < elem.childNodes.length; i++) {
            if (elem.childNodes[i].nodeType == Strophe.ElementType.TEXT) {
                str += elem.childNodes[i].nodeValue;
            }
        }
        return str;
    }, copyElement: function (elem) {
        var i, el;
        if (elem.nodeType == Strophe.ElementType.NORMAL) {
            el = Strophe.xmlElement(elem.tagName);
            for (i = 0; i < elem.attributes.length; i++) {
                el.setAttribute(elem.attributes[i].nodeName.toLowerCase(), elem.attributes[i].value);
            }
            for (i = 0; i < elem.childNodes.length; i++) {
                el.appendChild(Strophe.copyElement(elem.childNodes[i]));
            }
        } else if (elem.nodeType == Strophe.ElementType.TEXT) {
            el = Strophe.xmlGenerator().createTextNode(elem.nodeValue);
        }
        return el;
    }, escapeNode: function (node) {
        return node.replace(/^\s+|\s+$/g, '').replace(/\\/g, "\\5c")
            .replace(new RegExp(" ", "g"), "\\20")
            .replace(/\"/g, "\\22")
            .replace(/\&/g, "\\26")
            .replace(/\'/g, "\\27")
            .replace(/\//g, "\\2f")
            .replace(/:/g, "\\3a")
            .replace(/</g, "\\3c")
            .replace(/>/g, "\\3e")
            .replace(/@/g, "\\40");
    },

        /** Function: unescapeNode
         *  Unescape a node part (also called local part) of a JID.
         *
         *  Parameters:
         *    (String) node - A node (or local part).
         *
         *  Returns:
         *    An unescaped node (or local part).
         */
        unescapeNode: function (node) {
            return node.replace(/\\20/g, "")
                .replace(/\\22/g, '"')
                .replace(/\\26/g, "&")
                .replace(/\\27/g, "'")
                .replace(/\\2f/g, "/")
                .replace(/\\3a/g, ":")
                .replace(/\\3c/g, "<")
                .replace(/\\3e/g, ">")
                .replace(/\\40/g, "@")
                .replace(/\\5c/g, "\\");
        },

        /** Function: getNodeFromJid
         *  Get the node portion of a JID String.
         *
         *  Parameters:
         *    (String) jid - A JID.
         *
         *  Returns:
         *    A String containing the node.
         */
        getNodeFromJid: function (jid) {
            if (jid.indexOf("@") < 0) {
                return null;
            }
            return jid.split("@")[0];
        },

        /** Function: getDomainFromJid
         *  Get the domain portion of a JID String.
         *
         *  Parameters:
         *    (String) jid - A JID.
         *
         *  Returns:
         *    A String containing the domain.
         */
        getDomainFromJid: function (jid) {
            var bare = Strophe.getBareJidFromJid(jid);
            if (bare.indexOf("@") < 0) {
                return bare;
            } else {
                var parts = bare.split("@");
                parts.splice(0, 1);
                return parts.join('@');
            }
        },

        /** Function: getResourceFromJid
         *  Get the resource portion of a JID String.
         *
         *  Parameters:
         *    (String) jid - A JID.
         *
         *  Returns:
         *    A String containing the resource.
         */
        getResourceFromJid: function (jid) {
            var s = jid.split("/");
            if (s.length < 2) {
                return null;
            }
            s.splice(0, 1);
            return s.join('/');
        },

        /** Function: getBareJidFromJid
         *  Get the bare JID from a JID String.
         *
         *  Parameters:
         *    (String) jid - A JID.
         *
         *  Returns:
         *    A String containing the bare JID.
         */
        getBareJidFromJid: function (jid) {
            return jid ? jid.split("/")[0] : null;
        },

        /** Function: log
         *  User overrideable logging function.
         *
         *  This function is called whenever the Strophe library calls any
         *  of the logging functions.  The default implementation of this
         *  function does nothing.  If client code wishes to handle the logging
         *  messages, it should override this with
         *  > Strophe.log = function (level, msg) {
     *  >   (user code here)
     *  > };
         *
         *  Please note that data sent and received over the wire is logged
         *  via Strophe.Connection.rawInput() and Strophe.Connection.rawOutput().
         *
         *  The different levels and their meanings are
         *
         *    DEBUG - Messages useful for debugging purposes.
         *    INFO - Informational messages.  This is mostly information like
         *      'disconnect was called' or 'SASL auth succeeded'.
         *    WARN - Warnings about potential problems.  This is mostly used
         *      to report transient connection errors like request timeouts.
         *    ERROR - Some error occurred.
         *    FATAL - A non-recoverable fatal error occurred.
         *
         *  Parameters:
         *    (Integer) level - The log level of the log message.  This will
         *      be one of the values in Strophe.LogLevel.
         *    (String) msg - The log message.
         */
        log: function (level, msg) {
            return;
        },

        /** Function: debug
         *  Log a message at the Strophe.LogLevel.DEBUG level.
         *
         *  Parameters:
         *    (String) msg - The log message.
         */
        debug: function (msg) {
            this.log(this.LogLevel.DEBUG, msg);
        },

        /** Function: info
         *  Log a message at the Strophe.LogLevel.INFO level.
         *
         *  Parameters:
         *    (String) msg - The log message.
         */
        info: function (msg) {
            this.log(this.LogLevel.INFO, msg);
        },

        /** Function: warn
         *  Log a message at the Strophe.LogLevel.WARN level.
         *
         *  Parameters:
         *    (String) msg - The log message.
         */
        warn: function (msg) {
            this.log(this.LogLevel.WARN, msg);
        },

        /** Function: error
         *  Log a message at the Strophe.LogLevel.ERROR level.
         *
         *  Parameters:
         *    (String) msg - The log message.
         */
        error: function (msg) {
            this.log(this.LogLevel.ERROR, msg);
        },

        /** Function: fatal
         *  Log a message at the Strophe.LogLevel.FATAL level.
         *
         *  Parameters:
         *    (String) msg - The log message.
         */
        fatal: function (msg) {
            this.log(this.LogLevel.FATAL, msg);
        },

        /** Function: serialize
         *  Render a DOM element and all descendants to a String.
         *
         *  Parameters:
         *    (XMLElement) elem - A DOM element.
         *
         *  Returns:
         *    The serialized element tree as a String.
         */
        serialize: function (elem) {
            var result;

            if (!elem) {
                return null;
            }

            if (typeof(elem.tree) === "function") {
                elem = elem.tree();
            }

            var nodeName = elem.nodeName;
            var i, child;

            if (elem.getAttribute("_realname")) {
                nodeName = elem.getAttribute("_realname");
            }

            result = "<" + nodeName;
            for (i = 0; i < elem.attributes.length; i++) {
                if (elem.attributes[i].nodeName != "_realname") {
                    result += "" + elem.attributes[i].nodeName.toLowerCase() +
                        "='" + elem.attributes[i].value
                        .replace(/&/g, "&amp;")
                        .replace(/\'/g, "&apos;")
                        .replace(/</g, "&lt;") + "'";
                }
            }

            if (elem.childNodes.length > 0) {
                result += ">";
                for (i = 0; i < elem.childNodes.length; i++) {
                    child = elem.childNodes[i];
                    switch (child.nodeType) {
                        case Strophe.ElementType.NORMAL:
                            // normal element, so recurse
                            result += Strophe.serialize(child);
                            break;
                        case Strophe.ElementType.TEXT:
                            // text element to escape values
                            result += Strophe.xmlescape(child.nodeValue);
                            break;
                        case Strophe.ElementType.CDATA:
                            // cdata section so don't escape values
                            result += "<![CDATA[" + child.nodeValue + "]]>";
                    }
                }
                result += "</" + nodeName + ">";
            } else {
                result += "/>";
            }

            return result;
        },

        /** PrivateVariable: _requestId
         *  _Private_ variable that keeps track of the request ids for
         *  connections.
         */
        _requestId: 0,

        /** PrivateVariable: Strophe.connectionPlugins
         *  _Private_ variable Used to store plugin names that need
         *  initialization on Strophe.Connection construction.
         */
        _connectionPlugins: {},

        /** Function: addConnectionPlugin
         *  Extends the Strophe.Connection object with the given plugin.
         *
         *  Parameters:
         *    (String) name - The name of the extension.
         *    (Object) ptype - The plugin's prototype.
         */
        addConnectionPlugin: function (name, ptype) {
            Strophe._connectionPlugins[name] = ptype;
        }
    };

    /** Class: Strophe.Builder
     *  XML DOM builder.
     *
     *  This object provides an interface similar to JQuery but for building
     *  DOM element easily and rapidly.  All the functions except for toString()
     *  and tree() return the object, so calls can be chained.  Here's an
     *  example using the $iq() builder helper.
     *  > $iq({to: 'you', from: 'me', type: 'get', id: '1'})
     *  >     .c('query', {xmlns: 'strophe:example'})
     *  >     .c('example')
     *  >     .toString()
     *  The above generates this XML fragment
     *  > <iq to='you' from='me' type='get' id='1'>
     *  >   <query xmlns='strophe:example'>
     *  >     <example/>
     *  >   </query>
     *  > </iq>
     *  The corresponding DOM manipulations to get a similar fragment would be
     *  a lot more tedious and probably involve several helper variables.
     *
     *  Since adding children makes new operations operate on the child, up()
     *  is provided to traverse up the tree.  To add two children, do
     *  > builder.c('child1', ...).up().c('child2', ...)
     *  The next operation on the Builder will be relative to the second child.
     */

    /** Constructor: Strophe.Builder
     *  Create a Strophe.Builder object.
     *
     *  The attributes should be passed in object notation.  For example
     *  > var b = new Builder('message', {to: 'you', from: 'me'});
     *  or
     *  > var b = new Builder('messsage', {'xml:lang': 'en'});
     *
     *  Parameters:
     *    (String) name - The name of the root element.
     *    (Object) attrs - The attributes for the root element in object notation.
     *
     *  Returns:
     *    A new Strophe.Builder.
     */
    Strophe.Builder = function (name, attrs) {
        // Set correct namespace for jabber:client elements
        if (name == "presence" || name == "message" || name == "iq") {
            if (attrs && !attrs.xmlns) {
                attrs.xmlns = Strophe.NS.CLIENT;
            } else if (!attrs) {
                attrs = {xmlns: Strophe.NS.CLIENT};
            }
        }

        // Holds the tree being built.
        this.nodeTree = Strophe.xmlElement(name, attrs);

        // Points to the current operation node.
        this.node = this.nodeTree;
    };

    Strophe.Builder.prototype = {
        /** Function: tree
         *  Return the DOM tree.
         *
         *  This function returns the current DOM tree as an element object.  This
         *  is suitable for passing to functions like Strophe.Connection.send().
         *
         *  Returns:
         *    The DOM tree as a element object.
         */
        tree: function () {
            return this.nodeTree;
        },

        /** Function: toString
         *  Serialize the DOM tree to a String.
         *
         *  This function returns a string serialization of the current DOM
         *  tree.  It is often used internally to pass data to a
         *  Strophe.Request object.
         *
         *  Returns:
         *    The serialized DOM tree in a String.
         */
        toString: function () {
            return Strophe.serialize(this.nodeTree);
        },

        /** Function: up
         *  Make the current parent element the new current element.
         *
         *  This function is often used after c() to traverse back up the tree.
         *  For example, to add two children to the same element
         *  > builder.c('child1', {}).up().c('child2', {});
         *
         *  Returns:
         *    The Stophe.Builder object.
         */
        up: function () {
            this.node = this.node.parentNode;
            return this;
        },

        /** Function: attrs
         *  Add or modify attributes of the current element.
         *
         *  The attributes should be passed in object notation.  This function
         *  does not move the current element pointer.
         *
         *  Parameters:
         *    (Object) moreattrs - The attributes to add/modify in object notation.
         *
         *  Returns:
         *    The Strophe.Builder object.
         */
        attrs: function (moreattrs) {
            for (var k in moreattrs) {
                if (moreattrs.hasOwnProperty(k)) {
                    this.node.setAttribute(k, moreattrs[k]);
                }
            }
            return this;
        },

        /** Function: c
         *  Add a child to the current element and make it the new current
         *  element.
         *
         *  This function moves the current element pointer to the child,
         *  unless text is provided.  If you need to add another child, it
         *  is necessary to use up() to go back to the parent in the tree.
         *
         *  Parameters:
         *    (String) name - The name of the child.
         *    (Object) attrs - The attributes of the child in object notation.
         *    (String) text - The text to add to the child.
         *
         *  Returns:
         *    The Strophe.Builder object.
         */
        c: function (name, attrs, text) {
            var child = Strophe.xmlElement(name, attrs, text);
            this.node.appendChild(child);
            if (!text) {
                this.node = child;
            }
            return this;
        },

        /** Function: cnode
         *  Add a child to the current element and make it the new current
         *  element.
         *
         *  This function is the same as c() except that instead of using a
         *  name and an attributes object to create the child it uses an
         *  existing DOM element object.
         *
         *  Parameters:
         *    (XMLElement) elem - A DOM element.
         *
         *  Returns:
         *    The Strophe.Builder object.
         */
        cnode: function (elem) {
            var xmlGen = Strophe.xmlGenerator();
            try {
                var impNode = (xmlGen.importNode !== undefined);
            }
            catch (e) {
                var impNode = false;
            }
            var newElem = impNode ?
                xmlGen.importNode(elem, true) :
                Strophe.copyElement(elem);
            this.node.appendChild(newElem);
            this.node = newElem;
            return this;
        },

        /** Function: t
         *  Add a child text element.
         *
         *  This *does not* make the child the new current element since there
         *  are no children of text elements.
         *
         *  Parameters:
         *    (String) text - The text data to append to the current element.
         *
         *  Returns:
         *    The Strophe.Builder object.
         */
        t: function (text) {
            var child = Strophe.xmlTextNode(text);
            this.node.appendChild(child);
            return this;
        }
    };


    /** PrivateClass: Strophe.Handler
     *  _Private_ helper class for managing stanza handlers.
     *
     *  A Strophe.Handler encapsulates a user provided callback function to be
     *  executed when matching stanzas are received by the connection.
     *  Handlers can be either one-off or persistant depending on their
     *  return value. Returning true will cause a Handler to remain active, and
     *  returning false will remove the Handler.
     *
     *  Users will not use Strophe.Handler objects directly, but instead they
     *  will use Strophe.Connection.addHandler() and
     *  Strophe.Connection.deleteHandler().
     */

    /** PrivateConstructor: Strophe.Handler
     *  Create and initialize a new Strophe.Handler.
     *
     *  Parameters:
     *    (Function) handler - A function to be executed when the handler is run.
     *    (String) ns - The namespace to match.
     *    (String) name - The element name to match.
     *    (String) type - The element type to match.
     *    (String) id - The element id attribute to match.
     *    (String) from - The element from attribute to match.
     *    (Object) options - Handler options
     *
     *  Returns:
     *    A new Strophe.Handler object.
     */
    Strophe.Handler = function (handler, ns, name, type, id, from, options) {
        this.handler = handler;
        this.ns = ns;
        this.name = name;
        this.type = type;
        this.id = id;
        this.options = options || {matchbare: false};

        // default matchBare to false if undefined
        if (!this.options.matchBare) {
            this.options.matchBare = false;
        }

        if (this.options.matchBare) {
            this.from = from ? Strophe.getBareJidFromJid(from) : null;
        } else {
            this.from = from;
        }

        // whether the handler is a user handler or a system handler
        this.user = true;
    };

    Strophe.Handler.prototype = {
        /** PrivateFunction: isMatch
         *  Tests if a stanza matches the Strophe.Handler.
         *
         *  Parameters:
         *    (XMLElement) elem - The XML element to test.
         *
         *  Returns:
         *    true if the stanza matches and false otherwise.
         */
        isMatch: function (elem) {
            var nsMatch;
            var from = null;

            if (this.options.matchBare) {
                from = Strophe.getBareJidFromJid(elem.getAttribute('from'));
            } else {
                from = elem.getAttribute('from');
            }

            nsMatch = false;
            if (!this.ns) {
                nsMatch = true;
            } else {
                var that = this;
                Strophe.forEachChild(elem, null, function (elem) {
                    if (elem.getAttribute("xmlns") == that.ns) {
                        nsMatch = true;
                    }
                });

                nsMatch = nsMatch || elem.getAttribute("xmlns") == this.ns;
            }

            if (nsMatch &&
                (!this.name || Strophe.isTagEqual(elem, this.name)) &&
                (!this.type || elem.getAttribute("type") == this.type) &&
                (!this.id || elem.getAttribute("id") == this.id) &&
                (!this.from || from == this.from)) {
                return true;
            }

            return false;
        },

        /** PrivateFunction: run
         *  Run the callback on a matching stanza.
         *
         *  Parameters:
         *    (XMLElement) elem - The DOM element that triggered the
         *      Strophe.Handler.
         *
         *  Returns:
         *    A boolean indicating if the handler should remain active.
         */
        run: function (elem) {
            var result = null;
            try {
                result = this.handler(elem);
            } catch (e) {
                if (e.sourceURL) {
                    Strophe.fatal("error:" + this.handler +
                        "" + e.sourceURL + ":" +
                        e.line + "-" + e.name + ":" + e.message);
                } else if (e.fileName) {
                    if (typeof(console) != "undefined") {
                        console.trace();
                        console.error(this.handler, "-error-", e, e.message);
                    }
                    Strophe.fatal("error:" + this.handler + "" +
                        e.fileName + ":" + e.lineNumber + "-" +
                        e.name + ":" + e.message);
                } else {
                    Strophe.fatal("error:" + this.handler);
                }

                throw e;
            }

            return result;
        },

        /** PrivateFunction: toString
         *  Get a String representation of the Strophe.Handler object.
         *
         *  Returns:
         *    A String.
         */
        toString: function () {
            return "{Handler:" + this.handler + "(" + this.name + "," +
                this.id + "," + this.ns + ")}";
        }
    };

    /** PrivateClass: Strophe.TimedHandler
     *  _Private_ helper class for managing timed handlers.
     *
     *  A Strophe.TimedHandler encapsulates a user provided callback that
     *  should be called after a certain period of time or at regular
     *  intervals.  The return value of the callback determines whether the
     *  Strophe.TimedHandler will continue to fire.
     *
     *  Users will not use Strophe.TimedHandler objects directly, but instead
     *  they will use Strophe.Connection.addTimedHandler() and
     *  Strophe.Connection.deleteTimedHandler().
     */

    /** PrivateConstructor: Strophe.TimedHandler
     *  Create and initialize a new Strophe.TimedHandler object.
     *
     *  Parameters:
     *    (Integer) period - The number of milliseconds to wait before the
     *      handler is called.
     *    (Function) handler - The callback to run when the handler fires.  This
     *      function should take no arguments.
     *
     *  Returns:
     *    A new Strophe.TimedHandler object.
     */
    Strophe.TimedHandler = function (period, handler) {
        this.period = period;
        this.handler = handler;

        this.lastCalled = new Date().getTime();
        this.user = true;
    };

    Strophe.TimedHandler.prototype = {
        /** PrivateFunction: run
         *  Run the callback for the Strophe.TimedHandler.
         *
         *  Returns:
         *    true if the Strophe.TimedHandler should be called again, and false
         *      otherwise.
         */
        run: function () {
            this.lastCalled = new Date().getTime();
            return this.handler();
        },

        /** PrivateFunction: reset
         *  Reset the last called time for the Strophe.TimedHandler.
         */
        reset: function () {
            this.lastCalled = new Date().getTime();
        },

        /** PrivateFunction: toString
         *  Get a string representation of the Strophe.TimedHandler object.
         *
         *  Returns:
         *    The string representation.
         */
        toString: function () {
            return "{TimedHandler:" + this.handler + "(" + this.period + ")}";
        }
    };

    /** PrivateClass: Strophe.Request
     *  _Private_ helper class that provides a cross implementation abstraction
     *  for a BOSH related XMLHttpRequest.
     *
     *  The Strophe.Request class is used internally to encapsulate BOSH request
     *  information.  It is not meant to be used from user's code.
     */

    /** PrivateConstructor: Strophe.Request
     *  Create and initialize a new Strophe.Request object.
     *
     *  Parameters:
     *    (XMLElement) elem - The XML data to be sent in the request.
     *    (Function) func - The function that will be called when the
     *      XMLHttpRequest readyState changes.
     *    (Integer) rid - The BOSH rid attribute associated with this request.
     *    (Integer) sends - The number of times this same request has been
     *      sent.
     */
    Strophe.Request = function (elem, func, rid, sends) {
        this.id = ++Strophe._requestId;
        this.xmlData = elem;
        this.data = Strophe.serialize(elem);
        // save original function in case we need to make a new request
        // from this one.
        this.origFunc = func;
        this.func = func;
        this.rid = rid;
        this.date = NaN;
        this.sends = sends || 0;
        this.abort = false;
        this.dead = null;
        this.age = function () {
            if (!this.date) {
                return 0;
            }
            var now = new Date();
            return (now - this.date) / 1000;
        };
        this.timeDead = function () {
            if (!this.dead) {
                return 0;
            }
            var now = new Date();
            return (now - this.dead) / 1000;
        };
        this.xhr = this._newXHR();
    };

    Strophe.Request.prototype = {
        /** PrivateFunction: getResponse
         *  Get a response from the underlying XMLHttpRequest.
         *
         *  This function attempts to get a response from the request and checks
         *  for errors.
         *
         *  Throws:
         *    "parsererror" - A parser error occured.
         *
         *  Returns:
         *    The DOM element tree of the response.
         */
        getResponse: function () {
            var node = null;
            if (this.xhr.responseXML && this.xhr.responseXML.documentElement) {
                node = this.xhr.responseXML.documentElement;
                if (node.tagName == "parsererror") {
                    Strophe.error("invalid response received");
                    Strophe.error("responseText:" + this.xhr.responseText);
                    Strophe.error("responseXML:" +
                        Strophe.serialize(this.xhr.responseXML));
                    throw "parsererror";
                }
            } else if (this.xhr.responseText) {
                Strophe.error("invalid response received");
                Strophe.error("responseText:" + this.xhr.responseText);
                Strophe.error("responseXML:" +
                    Strophe.serialize(this.xhr.responseXML));
            }

            return node;
        },

        /** PrivateFunction: _newXHR
         *  _Private_ helper function to create XMLHttpRequests.
         *
         *  This function creates XMLHttpRequests across all implementations.
         *
         *  Returns:
         *    A new XMLHttpRequest.
         */
        _newXHR: function () {
            var xhr = null;
            if (window.XMLHttpRequest) {
                xhr = new XMLHttpRequest();
                if (xhr.overrideMimeType) {
                    xhr.overrideMimeType("text/xml");
                }
            } else if (window.ActiveXObject) {
                xhr = new ActiveXObject("Microsoft.XMLHTTP");
            }

            // use Function.bind() to prepend ourselves as an argument
            xhr.onreadystatechange = this.func.bind(null, this);

            return xhr;
        }
    };

    /** Class: Strophe.Connection
     *  XMPP Connection manager.
     *
     *  Thie class is the main part of Strophe.  It manages a BOSH connection
     *  to an XMPP server and dispatches events to the user callbacks as
     *  data arrives.  It supports SASL PLAIN, SASL DIGEST-MD5, and legacy
     *  authentication.
     *
     *  After creating a Strophe.Connection object, the user will typically
     *  call connect() with a user supplied callback to handle connection level
     *  events like authentication failure, disconnection, or connection
     *  complete.
     *
     *  The user will also have several event handlers defined by using
     *  addHandler() and addTimedHandler().  These will allow the user code to
     *  respond to interesting stanzas or do something periodically with the
     *  connection.  These handlers will be active once authentication is
     *  finished.
     *
     *  To send data to the connection, use send().
     */

    /** Constructor: Strophe.Connection
     *  Create and initialize a Strophe.Connection object.
     *
     *  Parameters:
     *    (String) service - The BOSH service URL.
     *
     *  Returns:
     *    A new Strophe.Connection object.
     */
    Strophe.Connection = function (service) {
        /* The path to the httpbind service. */
        this.service = service;
        /* The connected JID. */
        this.jid = "";
        /* request id for body tags */
        this.rid = Math.floor(Math.random() * 4294967295);
        /* The current session ID. */
        this.sid = null;
        this.streamId = null;
        /* stream:features */
        this.features = null;

        // SASL
        this.do_session = false;
        this.do_bind = false;

        // handler lists
        this.timedHandlers = [];
        this.handlers = [];
        this.removeTimeds = [];
        this.removeHandlers = [];
        this.addTimeds = [];
        this.addHandlers = [];

        this._idleTimeout = null;
        this._disconnectTimeout = null;

        this.authenticated = false;
        this.disconnecting = false;
        this.connected = false;

        this.errors = 0;

        this.paused = false;

        // default BOSH values
        this.hold = 1;
        this.wait = 60;
        this.window = 5;

        this._data = [];
        this._requests = [];
        this._uniqueId = Math.round(Math.random() * 10000);

        this._sasl_success_handler = null;
        this._sasl_failure_handler = null;
        this._sasl_challenge_handler = null;

        // setup onIdle callback every 1/10th of a second
        this._idleTimeout = setTimeout(this._onIdle.bind(this), 100);

        // initialize plugins
        for (var k in Strophe._connectionPlugins) {
            if (Strophe._connectionPlugins.hasOwnProperty(k)) {
                var ptype = Strophe._connectionPlugins[k];
                // jslint complaints about the below line, but this is fine
                var F = function () {
                };
                F.prototype = ptype;
                this[k] = new F();
                this[k].init(this);
            }
        }
    };

    Strophe.Connection.prototype = {
        /** Function: reset
         *  Reset the connection.
         *
         *  This function should be called after a connection is disconnected
         *  before that connection is reused.
         */
        reset: function () {
            this.rid = Math.floor(Math.random() * 4294967295);

            this.sid = null;
            this.streamId = null;

            // SASL
            this.do_session = false;
            this.do_bind = false;

            // handler lists
            this.timedHandlers = [];
            this.handlers = [];
            this.removeTimeds = [];
            this.removeHandlers = [];
            this.addTimeds = [];
            this.addHandlers = [];

            this.authenticated = false;
            this.disconnecting = false;
            this.connected = false;

            this.errors = 0;

            this._requests = [];
            this._uniqueId = Math.round(Math.random() * 10000);
        },

        /** Function: pause
         *  Pause the request manager.
         *
         *  This will prevent Strophe from sending any more requests to the
         *  server.  This is very useful for temporarily pausing while a lot
         *  of send() calls are happening quickly.  This causes Strophe to
         *  send the data in a single request, saving many request trips.
         */
        pause: function () {
            this.paused = true;
        },

        /** Function: resume
         *  Resume the request manager.
         *
         *  This resumes after pause() has been called.
         */
        resume: function () {
            this.paused = false;
        },

        /** Function: getUniqueId
         *  Generate a unique ID for use in <iq/> elements.
         *
         *  All <iq/> stanzas are required to have unique id attributes.  This
         *  function makes creating these easy.  Each connection instance has
         *  a counter which starts from zero, and the value of this counter
         *  plus a colon followed by the suffix becomes the unique id. If no
         *  suffix is supplied, the counter is used as the unique id.
         *
         *  Suffixes are used to make debugging easier when reading the stream
         *  data, and their use is recommended.  The counter resets to 0 for
         *  every new connection for the same reason.  For connections to the
         *  same server that authenticate the same way, all the ids should be
         *  the same, which makes it easy to see changes.  This is useful for
         *  automated testing as well.
         *
         *  Parameters:
         *    (String) suffix - A optional suffix to append to the id.
         *
         *  Returns:
         *    A unique string to be used for the id attribute.
         */
        getUniqueId: function (suffix) {
            if (typeof(suffix) == "string" || typeof(suffix) == "number") {
                return ++this._uniqueId + ":" + suffix;
            } else {
                return ++this._uniqueId + "";
            }
        },

        /** Function: connect
         *  Starts the connection process.
         *
         *  As the connection process proceeds, the user supplied callback will
         *  be triggered multiple times with status updates.  The callback
         *  should take two arguments - the status code and the error condition.
         *
         *  The status code will be one of the values in the Strophe.Status
         *  constants.  The error condition will be one of the conditions
         *  defined in RFC 3920 or the condition 'strophe-parsererror'.
         *
         *  Please see XEP 124 for a more detailed explanation of the optional
         *  parameters below.
         *
         *  Parameters:
         *    (String) jid - The user's JID.  This may be a bare JID,
         *      or a full JID.  If a node is not supplied, SASL ANONYMOUS
         *      authentication will be attempted.
         *    (String) pass - The user's password.
         *    (Function) callback - The connect callback function.
         *    (Integer) wait - The optional HTTPBIND wait value.  This is the
         *      time the server will wait before returning an empty result for
         *      a request.  The default setting of 60 seconds is recommended.
         *      Other settings will require tweaks to the Strophe.TIMEOUT value.
         *    (Integer) hold - The optional HTTPBIND hold value.  This is the
         *      number of connections the server will hold at one time.  This
         *      should almost always be set to 1 (the default).
         */
        connect: function (jid, pass, callback, wait, hold) {
            this.jid = jid;
            this.pass = pass;
            this.connect_callback = callback;
            this.disconnecting = false;
            this.connected = false;
            this.authenticated = false;
            this.errors = 0;

            this.wait = wait || this.wait;
            this.hold = hold || this.hold;

            // parse jid for domain and resource
            this.domain = Strophe.getDomainFromJid(this.jid);

            // build the body tag
            var body = this._buildBody().attrs({
                to: this.domain,
                "xml:lang": "en",
                wait: this.wait,
                hold: this.hold,
                content: "text/xml;charset=utf-8",
                ver: "1.6",
                "xmpp:version": "1.0",
                "xmlns:xmpp": Strophe.NS.BOSH
            });

            this._changeConnectStatus(Strophe.Status.CONNECTING, null);

            this._requests.push(
                new Strophe.Request(body.tree(),
                    this._onRequestStateChange.bind(
                        this, this._connect_cb.bind(this)),
                    body.tree().getAttribute("rid")));
            this._throttledRequestHandler();
        },

        /** Function: attach
         *  Attach to an already created and authenticated BOSH session.
         *
         *  This function is provided to allow Strophe to attach to BOSH
         *  sessions which have been created externally, perhaps by a Web
         *  application.  This is often used to support auto-login type features
         *  without putting user credentials into the page.
         *
         *  Parameters:
         *    (String) jid - The full JID that is bound by the session.
         *    (String) sid - The SID of the BOSH session.
         *    (String) rid - The current RID of the BOSH session.  This RID
         *      will be used by the next request.
         *    (Function) callback The connect callback function.
         *    (Integer) wait - The optional HTTPBIND wait value.  This is the
         *      time the server will wait before returning an empty result for
         *      a request.  The default setting of 60 seconds is recommended.
         *      Other settings will require tweaks to the Strophe.TIMEOUT value.
         *    (Integer) hold - The optional HTTPBIND hold value.  This is the
         *      number of connections the server will hold at one time.  This
         *      should almost always be set to 1 (the default).
         *    (Integer) wind - The optional HTTBIND window value.  This is the
         *      allowed range of request ids that are valid.  The default is 5.
         */
        attach: function (jid, sid, rid, callback, wait, hold, wind) {
            this.jid = jid;
            this.sid = sid;
            this.rid = rid;
            this.connect_callback = callback;

            this.domain = Strophe.getDomainFromJid(this.jid);

            this.authenticated = true;
            this.connected = true;

            this.wait = wait || this.wait;
            this.hold = hold || this.hold;
            this.window = wind || this.window;

            this._changeConnectStatus(Strophe.Status.ATTACHED, null);
        },

        /** Function: xmlInput
         *  User overrideable function that receives XML data coming into the
         *  connection.
         *
         *  The default function does nothing.  User code can override this with
         *  > Strophe.Connection.xmlInput = function (elem) {
     *  >   (user code)
     *  > };
         *
         *  Parameters:
         *    (XMLElement) elem - The XML data received by the connection.
         */
        xmlInput: function (elem) {
            return;
        },

        /** Function: xmlOutput
         *  User overrideable function that receives XML data sent to the
         *  connection.
         *
         *  The default function does nothing.  User code can override this with
         *  > Strophe.Connection.xmlOutput = function (elem) {
     *  >   (user code)
     *  > };
         *
         *  Parameters:
         *    (XMLElement) elem - The XMLdata sent by the connection.
         */
        xmlOutput: function (elem) {
            return;
        },

        /** Function: rawInput
         *  User overrideable function that receives raw data coming into the
         *  connection.
         *
         *  The default function does nothing.  User code can override this with
         *  > Strophe.Connection.rawInput = function (data) {
     *  >   (user code)
     *  > };
         *
         *  Parameters:
         *    (String) data - The data received by the connection.
         */
        rawInput: function (data) {
            return;
        },

        /** Function: rawOutput
         *  User overrideable function that receives raw data sent to the
         *  connection.
         *
         *  The default function does nothing.  User code can override this with
         *  > Strophe.Connection.rawOutput = function (data) {
     *  >   (user code)
     *  > };
         *
         *  Parameters:
         *    (String) data - The data sent by the connection.
         */
        rawOutput: function (data) {
            return;
        },

        /** Function: send
         *  Send a stanza.
         *
         *  This function is called to push data onto the send queue to
         *  go out over the wire.  Whenever a request is sent to the BOSH
         *  server, all pending data is sent and the queue is flushed.
         *
         *  Parameters:
         *    (XMLElement |
         *     [XMLElement] |
         *     Strophe.Builder) elem - The stanza to send.
         */
        send: function (elem) {
            if (elem === null) {
                return;
            }
            if (typeof(elem.sort) === "function") {
                for (var i = 0; i < elem.length; i++) {
                    this._queueData(elem[i]);
                }
            } else if (typeof(elem.tree) === "function") {
                this._queueData(elem.tree());
            } else {
                this._queueData(elem);
            }

            this._throttledRequestHandler();
            clearTimeout(this._idleTimeout);
            this._idleTimeout = setTimeout(this._onIdle.bind(this), 100);
        },

        /** Function: flush
         *  Immediately send any pending outgoing data.
         *
         *  Normally send() queues outgoing data until the next idle period
         *  (100ms), which optimizes network use in the common cases when
         *  several send()s are called in succession. flush() can be used to
         *  immediately send all pending data.
         */
        flush: function () {
            // cancel the pending idle period and run the idle function
            // immediately
            clearTimeout(this._idleTimeout);
            this._onIdle();
        },

        /** Function: sendIQ
         *  Helper function to send IQ stanzas.
         *
         *  Parameters:
         *    (XMLElement) elem - The stanza to send.
         *    (Function) callback - The callback function for a successful request.
         *    (Function) errback - The callback function for a failed or timed
         *      out request.  On timeout, the stanza will be null.
         *    (Integer) timeout - The time specified in milliseconds for a
         *      timeout to occur.
         *
         *  Returns:
         *    The id used to send the IQ.
         */
        sendIQ: function (elem, callback, errback, timeout) {
            var timeoutHandler = null;
            var that = this;

            if (typeof(elem.tree) === "function") {
                elem = elem.tree();
            }
            var id = elem.getAttribute('id');

            // inject id if not found
            if (!id) {
                id = this.getUniqueId("sendIQ");
                elem.setAttribute("id", id);
            }

            var handler = this.addHandler(function (stanza) {
                // remove timeout handler if there is one
                if (timeoutHandler) {
                    that.deleteTimedHandler(timeoutHandler);
                }

                var iqtype = stanza.getAttribute('type');
                if (iqtype == 'result') {
                    if (callback) {
                        callback(stanza);
                    }
                } else if (iqtype == 'error') {
                    if (errback) {
                        errback(stanza);
                    }
                } else {
                    throw {
                        name: "StropheError",
                        message: "Got bad IQ type of" + iqtype
                    };
                }
            }, null, 'iq', null, id);

            // if timeout specified, setup timeout handler.
            if (timeout) {
                timeoutHandler = this.addTimedHandler(timeout, function () {
                    // get rid of normal handler
                    that.deleteHandler(handler);

                    // call errback on timeout with null stanza
                    if (errback) {
                        errback(null);
                    }
                    return false;
                });
            }

            this.send(elem);

            return id;
        },

        /** PrivateFunction: _queueData
         *  Queue outgoing data for later sending.  Also ensures that the data
         *  is a DOMElement.
         */
        _queueData: function (element) {
            if (element === null || !element.tagName || !element.childNodes) {
                throw {
                    name: "StropheError",
                    message: "Cannot queue non-DOMElement."
                };
            }

            this._data.push(element);
        },

        /** PrivateFunction: _sendRestart
         *  Send an xmpp:restart stanza.
         */
        _sendRestart: function () {
            this._data.push("restart");

            this._throttledRequestHandler();
            clearTimeout(this._idleTimeout);
            this._idleTimeout = setTimeout(this._onIdle.bind(this), 100);
        },

        /** Function: addTimedHandler
         *  Add a timed handler to the connection.
         *
         *  This function adds a timed handler.  The provided handler will
         *  be called every period milliseconds until it returns false,
         *  the connection is terminated, or the handler is removed.  Handlers
         *  that wish to continue being invoked should return true.
         *
         *  Because of method binding it is necessary to save the result of
         *  this function if you wish to remove a handler with
         *  deleteTimedHandler().
         *
         *  Note that user handlers are not active until authentication is
         *  successful.
         *
         *  Parameters:
         *    (Integer) period - The period of the handler.
         *    (Function) handler - The callback function.
         *
         *  Returns:
         *    A reference to the handler that can be used to remove it.
         */
        addTimedHandler: function (period, handler) {
            var thand = new Strophe.TimedHandler(period, handler);
            this.addTimeds.push(thand);
            return thand;
        },

        /** Function: deleteTimedHandler
         *  Delete a timed handler for a connection.
         *
         *  This function removes a timed handler from the connection.  The
         *  handRef parameter is *not* the function passed to addTimedHandler(),
         *  but is the reference returned from addTimedHandler().
         *
         *  Parameters:
         *    (Strophe.TimedHandler) handRef - The handler reference.
         */
        deleteTimedHandler: function (handRef) {
            // this must be done in the Idle loop so that we don't change
            // the handlers during iteration
            this.removeTimeds.push(handRef);
        },

        /** Function: addHandler
         *  Add a stanza handler for the connection.
         *
         *  This function adds a stanza handler to the connection.  The
         *  handler callback will be called for any stanza that matches
         *  the parameters.  Note that if multiple parameters are supplied,
         *  they must all match for the handler to be invoked.
         *
         *  The handler will receive the stanza that triggered it as its argument.
         *  The handler should return true if it is to be invoked again;
         *  returning false will remove the handler after it returns.
         *
         *  As a convenience, the ns parameters applies to the top level element
         *  and also any of its immediate children.  This is primarily to make
         *  matching /iq/query elements easy.
         *
         *  The options argument contains handler matching flags that affect how
         *  matches are determined. Currently the only flag is matchBare (a
         *  boolean). When matchBare is true, the from parameter and the from
         *  attribute on the stanza will be matched as bare JIDs instead of
         *  full JIDs. To use this, pass {matchBare: true} as the value of
         *  options. The default value for matchBare is false.
         *
         *  The return value should be saved if you wish to remove the handler
         *  with deleteHandler().
         *
         *  Parameters:
         *    (Function) handler - The user callback.
         *    (String) ns - The namespace to match.
         *    (String) name - The stanza name to match.
         *    (String) type - The stanza type attribute to match.
         *    (String) id - The stanza id attribute to match.
         *    (String) from - The stanza from attribute to match.
         *    (String) options - The handler options
         *
         *  Returns:
         *    A reference to the handler that can be used to remove it.
         */
        addHandler: function (handler, ns, name, type, id, from, options) {
            var hand = new Strophe.Handler(handler, ns, name, type, id, from, options);
            this.addHandlers.push(hand);
            return hand;
        },

        /** Function: deleteHandler
         *  Delete a stanza handler for a connection.
         *
         *  This function removes a stanza handler from the connection.  The
         *  handRef parameter is *not* the function passed to addHandler(),
         *  but is the reference returned from addHandler().
         *
         *  Parameters:
         *    (Strophe.Handler) handRef - The handler reference.
         */
        deleteHandler: function (handRef) {
            // this must be done in the Idle loop so that we don't change
            // the handlers during iteration
            this.removeHandlers.push(handRef);
        },

        /** Function: disconnect
         *  Start the graceful disconnection process.
         *
         *  This function starts the disconnection process.  This process starts
         *  by sending unavailable presence and sending BOSH body of type
         *  terminate.  A timeout handler makes sure that disconnection happens
         *  even if the BOSH server does not respond.
         *
         *  The user supplied connection callback will be notified of the
         *  progress as this process happens.
         *
         *  Parameters:
         *    (String) reason - The reason the disconnect is occuring.
         */
        disconnect: function (reason) {
            this._changeConnectStatus(Strophe.Status.DISCONNECTING, reason);

            Strophe.info("Disconnect was called because:" + reason);
            if (this.connected) {
                // setup timeout handler
                this._disconnectTimeout = this._addSysTimedHandler(
                    3000, this._onDisconnectTimeout.bind(this));
                this._sendTerminate();
            }
        },

        /** PrivateFunction: _changeConnectStatus
         *  _Private_ helper function that makes sure plugins and the user's
         *  callback are notified of connection status changes.
         *
         *  Parameters:
         *    (Integer) status - the new connection status, one of the values
         *      in Strophe.Status
         *    (String) condition - the error condition or null
         */
        _changeConnectStatus: function (status, condition) {
            // notify all plugins listening for status changes
            for (var k in Strophe._connectionPlugins) {
                if (Strophe._connectionPlugins.hasOwnProperty(k)) {
                    var plugin = this[k];
                    if (plugin.statusChanged) {
                        try {
                            plugin.statusChanged(status, condition);
                        } catch (err) {
                            Strophe.error("" + k + "plugin caused an exception" +
                                "changing status:" + err);
                        }
                    }
                }
            }

            // notify the user's callback
            if (this.connect_callback) {
                try {
                    this.connect_callback(status, condition);
                } catch (e) {
                    Strophe.error("User connection callback caused an" +
                        "exception:" + e);
                }
            }
        },

        /** PrivateFunction: _buildBody
         *  _Private_ helper function to generate the <body/> wrapper for BOSH.
         *
         *  Returns:
         *    A Strophe.Builder with a <body/> element.
         */
        _buildBody: function () {
            var bodyWrap = $build('body', {
                rid: this.rid++,
                xmlns: Strophe.NS.HTTPBIND
            });

            if (this.sid !== null) {
                bodyWrap.attrs({sid: this.sid});
            }

            return bodyWrap;
        },

        /** PrivateFunction: _removeRequest
         *  _Private_ function to remove a request from the queue.
         *
         *  Parameters:
         *    (Strophe.Request) req - The request to remove.
         */
        _removeRequest: function (req) {
            Strophe.debug("removing request");

            var i;
            for (i = this._requests.length - 1; i >= 0; i--) {
                if (req == this._requests[i]) {
                    this._requests.splice(i, 1);
                }
            }

            // IE6 fails on setting to null, so set to empty function
            req.xhr.onreadystatechange = function () {
            };

            this._throttledRequestHandler();
        },

        /** PrivateFunction: _restartRequest
         *  _Private_ function to restart a request that is presumed dead.
         *
         *  Parameters:
         *    (Integer) i - The index of the request in the queue.
         */
        _restartRequest: function (i) {
            var req = this._requests[i];
            if (req.dead === null) {
                req.dead = new Date();
            }

            this._processRequest(i);
        },

        /** PrivateFunction: _processRequest
         *  _Private_ function to process a request in the queue.
         *
         *  This function takes requests off the queue and sends them and
         *  restarts dead requests.
         *
         *  Parameters:
         *    (Integer) i - The index of the request in the queue.
         */
        _processRequest: function (i) {
            var req = this._requests[i];
            var reqStatus = -1;

            try {
                if (req.xhr.readyState == 4) {
                    reqStatus = req.xhr.status;
                }
            } catch (e) {
                Strophe.error("caught an error in _requests[" + i +
                    "],reqStatus:" + reqStatus);
            }

            if (typeof(reqStatus) == "undefined") {
                reqStatus = -1;
            }

            // make sure we limit the number of retries
            if (req.sends > 5) {
                this._onDisconnectTimeout();
                return;
            }

            var time_elapsed = req.age();
            var primaryTimeout = (!isNaN(time_elapsed) &&
                time_elapsed > Math.floor(Strophe.TIMEOUT * this.wait));
            var secondaryTimeout = (req.dead !== null &&
                req.timeDead() > Math.floor(Strophe.SECONDARY_TIMEOUT * this.wait));
            var requestCompletedWithServerError = (req.xhr.readyState == 4 &&
                (reqStatus < 1 ||
                    reqStatus >= 500));
            if (primaryTimeout || secondaryTimeout ||
                requestCompletedWithServerError) {
                if (secondaryTimeout) {
                    Strophe.error("Request" +
                        this._requests[i].id +
                        "timed out(secondary),restarting");
                }
                req.abort = true;
                req.xhr.abort();
                // setting to null fails on IE6, so set to empty function
                req.xhr.onreadystatechange = function () {
                };
                this._requests[i] = new Strophe.Request(req.xmlData,
                    req.origFunc,
                    req.rid,
                    req.sends);
                req = this._requests[i];
            }

            if (req.xhr.readyState === 0) {
                Strophe.debug("request id" + req.id +
                    "." + req.sends + "posting");

                try {
                    req.xhr.open("POST", this.service, true);
                } catch (e2) {
                    Strophe.error("XHR open failed.");
                    if (!this.connected) {
                        this._changeConnectStatus(Strophe.Status.CONNFAIL,
                            "bad-service");
                    }
                    this.disconnect();
                    return;
                }

                // Fires the XHR request -- may be invoked immediately
                // or on a gradually expanding retry window for reconnects
                var sendFunc = function () {
                    req.date = new Date();
                    req.xhr.send(req.data);
                };

                // Implement progressive backoff for reconnects --
                // First retry (send == 1) should also be instantaneous
                if (req.sends > 1) {
                    // Using a cube of the retry number creates a nicely
                    // expanding retry window
                    var backoff = Math.min(Math.floor(Strophe.TIMEOUT * this.wait),
                        Math.pow(req.sends, 3)) * 1000;
                    setTimeout(sendFunc, backoff);
                } else {
                    sendFunc();
                }

                req.sends++;

                if (this.xmlOutput !== Strophe.Connection.prototype.xmlOutput) {
                    this.xmlOutput(req.xmlData);
                }
                if (this.rawOutput !== Strophe.Connection.prototype.rawOutput) {
                    this.rawOutput(req.data);
                }
            } else {
                Strophe.debug("_processRequest:" +
                    (i === 0 ? "first" : "second") +
                    "request has readyState of" +
                    req.xhr.readyState);
            }
        },

        /** PrivateFunction: _throttledRequestHandler
         *  _Private_ function to throttle requests to the connection window.
         *
         *  This function makes sure we don't send requests so fast that the
         *  request ids overflow the connection window in the case that one
         *  request died.
         */
        _throttledRequestHandler: function () {
            if (!this._requests) {
                Strophe.debug("_throttledRequestHandler called with" +
                    "undefined requests");
            } else {
                Strophe.debug("_throttledRequestHandler called with" +
                    this._requests.length + "requests");
            }

            if (!this._requests || this._requests.length === 0) {
                return;
            }

            if (this._requests.length > 0) {
                this._processRequest(0);
            }

            if (this._requests.length > 1 &&
                Math.abs(this._requests[0].rid -
                    this._requests[1].rid) < this.window) {
                this._processRequest(1);
            }
        },

        /** PrivateFunction: _onRequestStateChange
         *  _Private_ handler for Strophe.Request state changes.
         *
         *  This function is called when the XMLHttpRequest readyState changes.
         *  It contains a lot of error handling logic for the many ways that
         *  requests can fail, and calls the request callback when requests
         *  succeed.
         *
         *  Parameters:
         *    (Function) func - The handler for the request.
         *    (Strophe.Request) req - The request that is changing readyState.
         */
        _onRequestStateChange: function (func, req) {
            Strophe.debug("request id" + req.id +
                "." + req.sends + "state changed to" +
                req.xhr.readyState);

            if (req.abort) {
                req.abort = false;
                return;
            }

            // request complete
            var reqStatus;
            if (req.xhr.readyState == 4) {
                reqStatus = 0;
                try {
                    reqStatus = req.xhr.status;
                } catch (e) {
                    // ignore errors from undefined status attribute.  works
                    // around a browser bug
                }

                if (typeof(reqStatus) == "undefined") {
                    reqStatus = 0;
                }

                if (this.disconnecting) {
                    if (reqStatus >= 400) {
                        this._hitError(reqStatus);
                        return;
                    }
                }

                var reqIs0 = (this._requests[0] == req);
                var reqIs1 = (this._requests[1] == req);

                if ((reqStatus > 0 && reqStatus < 500) || req.sends > 5) {
                    // remove from internal queue
                    this._removeRequest(req);
                    Strophe.debug("request id" +
                        req.id +
                        "should now be removed");
                }

                // request succeeded
                if (reqStatus == 200) {
                    // if request 1 finished, or request 0 finished and request
                    // 1 is over Strophe.SECONDARY_TIMEOUT seconds old, we need to
                    // restart the other - both will be in the first spot, as the
                    // completed request has been removed from the queue already
                    if (reqIs1 ||
                        (reqIs0 && this._requests.length > 0 &&
                            this._requests[0].age() > Math.floor(Strophe.SECONDARY_TIMEOUT * this.wait))) {
                        this._restartRequest(0);
                    }
                    // call handler
                    Strophe.debug("request id" +
                        req.id + "." +
                        req.sends + "got 200");
                    func(req);
                    this.errors = 0;
                } else {
                    Strophe.error("request id" +
                        req.id + "." +
                        req.sends + "error" + reqStatus +
                        "happened");
                    if (reqStatus === 0 ||
                        (reqStatus >= 400 && reqStatus < 600) ||
                        reqStatus >= 12000) {
                        this._hitError(reqStatus);
                        if (reqStatus >= 400 && reqStatus < 500) {
                            this._changeConnectStatus(Strophe.Status.DISCONNECTING,
                                null);
                            this._doDisconnect();
                        }
                    }
                }

                if (!((reqStatus > 0 && reqStatus < 500) ||
                    req.sends > 5)) {
                    this._throttledRequestHandler();
                }
            }
        },

        /** PrivateFunction: _hitError
         *  _Private_ function to handle the error count.
         *
         *  Requests are resent automatically until their error count reaches
         *  5.  Each time an error is encountered, this function is called to
         *  increment the count and disconnect if the count is too high.
         *
         *  Parameters:
         *    (Integer) reqStatus - The request status.
         */
        _hitError: function (reqStatus) {
            this.errors++;
            Strophe.warn("request errored,status:" + reqStatus +
                ",number of errors:" + this.errors);
            if (this.errors > 4) {
                this._onDisconnectTimeout();
            }
        },

        /** PrivateFunction: _doDisconnect
         *  _Private_ function to disconnect.
         *
         *  This is the last piece of the disconnection logic.  This resets the
         *  connection and alerts the user's connection callback.
         */
        _doDisconnect: function () {
            Strophe.info("_doDisconnect was called");
            this.authenticated = false;
            this.disconnecting = false;
            this.sid = null;
            this.streamId = null;
            this.rid = Math.floor(Math.random() * 4294967295);

            // tell the parent we disconnected
            if (this.connected) {
                this._changeConnectStatus(Strophe.Status.DISCONNECTED, null);
                this.connected = false;
            }

            // delete handlers
            this.handlers = [];
            this.timedHandlers = [];
            this.removeTimeds = [];
            this.removeHandlers = [];
            this.addTimeds = [];
            this.addHandlers = [];
        },

        /** PrivateFunction: _dataRecv
         *  _Private_ handler to processes incoming data from the the connection.
         *
         *  Except for _connect_cb handling the initial connection request,
         *  this function handles the incoming data for all requests.  This
         *  function also fires stanza handlers that match each incoming
         *  stanza.
         *
         *  Parameters:
         *    (Strophe.Request) req - The request that has data ready.
         */
        _dataRecv: function (req) {
            try {
                var elem = req.getResponse();
            } catch (e) {
                if (e != "parsererror") {
                    throw e;
                }
                this.disconnect("strophe-parsererror");
            }
            if (elem === null) {
                return;
            }

            if (this.xmlInput !== Strophe.Connection.prototype.xmlInput) {
                this.xmlInput(elem);
            }
            if (this.rawInput !== Strophe.Connection.prototype.rawInput) {
                this.rawInput(Strophe.serialize(elem));
            }

            // remove handlers scheduled for deletion
            var i, hand;
            while (this.removeHandlers.length > 0) {
                hand = this.removeHandlers.pop();
                i = this.handlers.indexOf(hand);
                if (i >= 0) {
                    this.handlers.splice(i, 1);
                }
            }

            // add handlers scheduled for addition
            while (this.addHandlers.length > 0) {
                this.handlers.push(this.addHandlers.pop());
            }

            // handle graceful disconnect
            if (this.disconnecting && this._requests.length === 0) {
                this.deleteTimedHandler(this._disconnectTimeout);
                this._disconnectTimeout = null;
                this._doDisconnect();
                return;
            }

            var typ = elem.getAttribute("type");
            var cond, conflict;
            if (typ !== null && typ == "terminate") {
                // Don't process stanzas that come in after disconnect
                if (this.disconnecting) {
                    return;
                }

                // an error occurred
                cond = elem.getAttribute("condition");
                conflict = elem.getElementsByTagName("conflict");
                if (cond !== null) {
                    if (cond == "remote-stream-error" && conflict.length > 0) {
                        cond = "conflict";
                    }
                    this._changeConnectStatus(Strophe.Status.CONNFAIL, cond);
                } else {
                    this._changeConnectStatus(Strophe.Status.CONNFAIL, "unknown");
                }
                this.disconnect();
                return;
            }

            // send each incoming stanza through the handler chain
            var that = this;
            Strophe.forEachChild(elem, null, function (child) {
                var i, newList;
                // process handlers
                newList = that.handlers;
                that.handlers = [];
                for (i = 0; i < newList.length; i++) {
                    var hand = newList[i];
                    // encapsulate 'handler.run' not to lose the whole handler list if
                    // one of the handlers throws an exception
                    try {
                        if (hand.isMatch(child) &&
                            (that.authenticated || !hand.user)) {
                            if (hand.run(child)) {
                                that.handlers.push(hand);
                            }
                        } else {
                            that.handlers.push(hand);
                        }
                    } catch (e) {
                        //if the handler throws an exception, we consider it as false
                    }
                }
            });
        },

        /** PrivateFunction: _sendTerminate
         *  _Private_ function to send initial disconnect sequence.
         *
         *  This is the first step in a graceful disconnect.  It sends
         *  the BOSH server a terminate body and includes an unavailable
         *  presence if authentication has completed.
         */
        _sendTerminate: function () {
            Strophe.info("_sendTerminate was called");
            var body = this._buildBody().attrs({type: "terminate"});

            if (this.authenticated) {
                body.c('presence', {
                    xmlns: Strophe.NS.CLIENT,
                    type: 'unavailable'
                });
            }

            this.disconnecting = true;

            var req = new Strophe.Request(body.tree(),
                this._onRequestStateChange.bind(
                    this, this._dataRecv.bind(this)),
                body.tree().getAttribute("rid"));

            this._requests.push(req);
            this._throttledRequestHandler();
        },

        /** PrivateFunction: _connect_cb
         *  _Private_ handler for initial connection request.
         *
         *  This handler is used to process the initial connection request
         *  response from the BOSH server. It is used to set up authentication
         *  handlers and start the authentication process.
         *
         *  SASL authentication will be attempted if available, otherwise
         *  the code will fall back to legacy authentication.
         *
         *  Parameters:
         *    (Strophe.Request) req - The current request.
         */
        _connect_cb: function (req) {
            Strophe.info("_connect_cb was called");

            this.connected = true;
            var bodyWrap = req.getResponse();
            if (!bodyWrap) {
                return;
            }

            if (this.xmlInput !== Strophe.Connection.prototype.xmlInput) {
                this.xmlInput(bodyWrap);
            }
            if (this.rawInput !== Strophe.Connection.prototype.rawInput) {
                this.rawInput(Strophe.serialize(bodyWrap));
            }

            var typ = bodyWrap.getAttribute("type");
            var cond, conflict;
            if (typ !== null && typ == "terminate") {
                // an error occurred
                cond = bodyWrap.getAttribute("condition");
                conflict = bodyWrap.getElementsByTagName("conflict");
                if (cond !== null) {
                    if (cond == "remote-stream-error" && conflict.length > 0) {
                        cond = "conflict";
                    }
                    this._changeConnectStatus(Strophe.Status.CONNFAIL, cond);
                } else {
                    this._changeConnectStatus(Strophe.Status.CONNFAIL, "unknown");
                }
                return;
            }

            // check to make sure we don't overwrite these if _connect_cb is
            // called multiple times in the case of missing stream:features
            if (!this.sid) {
                this.sid = bodyWrap.getAttribute("sid");
            }
            if (!this.stream_id) {
                this.stream_id = bodyWrap.getAttribute("authid");
            }
            var wind = bodyWrap.getAttribute('requests');
            if (wind) {
                this.window = parseInt(wind, 10);
            }
            var hold = bodyWrap.getAttribute('hold');
            if (hold) {
                this.hold = parseInt(hold, 10);
            }
            var wait = bodyWrap.getAttribute('wait');
            if (wait) {
                this.wait = parseInt(wait, 10);
            }


            var do_sasl_plain = false;
            var do_sasl_digest_md5 = false;
            var do_sasl_anonymous = false;

            var mechanisms = bodyWrap.getElementsByTagName("mechanism");
            var i, mech, auth_str, hashed_auth_str;
            if (mechanisms.length > 0) {
                for (i = 0; i < mechanisms.length; i++) {
                    mech = Strophe.getText(mechanisms[i]);
                    if (mech == 'DIGEST-MD5') {
                        do_sasl_digest_md5 = true;
                    } else if (mech == 'PLAIN') {
                        do_sasl_plain = true;
                    } else if (mech == 'ANONYMOUS') {
                        do_sasl_anonymous = true;
                    }
                }
            } else {
                // we didn't get stream:features yet, so we need wait for it
                // by sending a blank poll request
                var body = this._buildBody();
                this._requests.push(
                    new Strophe.Request(body.tree(),
                        this._onRequestStateChange.bind(
                            this, this._connect_cb.bind(this)),
                        body.tree().getAttribute("rid")));
                this._throttledRequestHandler();
                return;
            }

            if (Strophe.getNodeFromJid(this.jid) === null &&
                do_sasl_anonymous) {
                this._changeConnectStatus(Strophe.Status.AUTHENTICATING, null);
                this._sasl_success_handler = this._addSysHandler(
                    this._sasl_success_cb.bind(this), null,
                    "success", null, null);
                this._sasl_failure_handler = this._addSysHandler(
                    this._sasl_failure_cb.bind(this), null,
                    "failure", null, null);

                this.send($build("auth", {
                    xmlns: Strophe.NS.SASL,
                    mechanism: "ANONYMOUS"
                }).tree());
            } else if (Strophe.getNodeFromJid(this.jid) === null) {
                // we don't have a node, which is required for non-anonymous
                // client connections
                this._changeConnectStatus(Strophe.Status.CONNFAIL,
                    'x-strophe-bad-non-anon-jid');
                this.disconnect();
            } else if (do_sasl_digest_md5) {
                this._changeConnectStatus(Strophe.Status.AUTHENTICATING, null);
                this._sasl_challenge_handler = this._addSysHandler(
                    this._sasl_challenge1_cb.bind(this), null,
                    "challenge", null, null);
                this._sasl_failure_handler = this._addSysHandler(
                    this._sasl_failure_cb.bind(this), null,
                    "failure", null, null);

                this.send($build("auth", {
                    xmlns: Strophe.NS.SASL,
                    mechanism: "DIGEST-MD5"
                }).tree());
            } else if (do_sasl_plain) {
                // Build the plain auth string (barejid null
                // username null password) and base 64 encoded.
                auth_str = Strophe.getBareJidFromJid(this.jid);
                auth_str = auth_str + "\u0000";
                auth_str = auth_str + Strophe.getNodeFromJid(this.jid);
                auth_str = auth_str + "\u0000";
                auth_str = auth_str + this.pass;

                this._changeConnectStatus(Strophe.Status.AUTHENTICATING, null);
                this._sasl_success_handler = this._addSysHandler(
                    this._sasl_success_cb.bind(this), null,
                    "success", null, null);
                this._sasl_failure_handler = this._addSysHandler(
                    this._sasl_failure_cb.bind(this), null,
                    "failure", null, null);

                hashed_auth_str = Base64.encode(auth_str);
                this.send($build("auth", {
                    xmlns: Strophe.NS.SASL,
                    mechanism: "PLAIN"
                }).t(hashed_auth_str).tree());
            } else {
                this._changeConnectStatus(Strophe.Status.AUTHENTICATING, null);
                this._addSysHandler(this._auth1_cb.bind(this), null, null,
                    null, "_auth_1");

                this.send($iq({
                    type: "get",
                    to: this.domain,
                    id: "_auth_1"
                }).c("query", {
                        xmlns: Strophe.NS.AUTH
                    }).c("username", {}).t(Strophe.getNodeFromJid(this.jid)).tree());
            }
        },

        /** PrivateFunction: _sasl_challenge1_cb
         *  _Private_ handler for DIGEST-MD5 SASL authentication.
         *
         *  Parameters:
         *    (XMLElement) elem - The challenge stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_challenge1_cb: function (elem) {
            var attribMatch = /([a-z]+)=("[^"]+"|[^,"]+)(?:,|$)/;

            var challenge = Base64.decode(Strophe.getText(elem));
            var cnonce = MD5.hexdigest("" + (Math.random() * 1234567890));
            var realm = "";
            var host = null;
            var nonce = "";
            var qop = "";
            var matches;

            // remove unneeded handlers
            this.deleteHandler(this._sasl_failure_handler);

            while (challenge.match(attribMatch)) {
                matches = challenge.match(attribMatch);
                challenge = challenge.replace(matches[0], "");
                matches[2] = matches[2].replace(/^"(.+)"$/, "$1");
                switch (matches[1]) {
                    case "realm":
                        realm = matches[2];
                        break;
                    case "nonce":
                        nonce = matches[2];
                        break;
                    case "qop":
                        qop = matches[2];
                        break;
                    case "host":
                        host = matches[2];
                        break;
                }
            }

            var digest_uri = "xmpp/" + this.domain;
            if (host !== null) {
                digest_uri = digest_uri + "/" + host;
            }

            var A1 = MD5.hash(Strophe.getNodeFromJid(this.jid) +
                ":" + realm + ":" + this.pass) +
                ":" + nonce + ":" + cnonce;
            var A2 = 'AUTHENTICATE:' + digest_uri;

            var responseText = "";
            responseText += 'username=' +
                this._quote(Strophe.getNodeFromJid(this.jid)) + ',';
            responseText += 'realm=' + this._quote(realm) + ',';
            responseText += 'nonce=' + this._quote(nonce) + ',';
            responseText += 'cnonce=' + this._quote(cnonce) + ',';
            responseText += 'nc="00000001",';
            responseText += 'qop="auth",';
            responseText += 'digest-uri=' + this._quote(digest_uri) + ',';
            responseText += 'response=' + this._quote(
                MD5.hexdigest(MD5.hexdigest(A1) + ":" +
                    nonce + ":00000001:" +
                    cnonce + ":auth:" +
                    MD5.hexdigest(A2))) + ',';
            responseText += 'charset="utf-8"';

            this._sasl_challenge_handler = this._addSysHandler(
                this._sasl_challenge2_cb.bind(this), null,
                "challenge", null, null);
            this._sasl_success_handler = this._addSysHandler(
                this._sasl_success_cb.bind(this), null,
                "success", null, null);
            this._sasl_failure_handler = this._addSysHandler(
                this._sasl_failure_cb.bind(this), null,
                "failure", null, null);

            this.send($build('response', {
                xmlns: Strophe.NS.SASL
            }).t(Base64.encode(responseText)).tree());

            return false;
        },

        /** PrivateFunction: _quote
         *  _Private_ utility function to backslash escape and quote strings.
         *
         *  Parameters:
         *    (String) str - The string to be quoted.
         *
         *  Returns:
         *    quoted string
         */
        _quote: function (str) {
            return '"' + str.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
            //" end string workaround for emacs
        },


        /** PrivateFunction: _sasl_challenge2_cb
         *  _Private_ handler for second step of DIGEST-MD5 SASL authentication.
         *
         *  Parameters:
         *    (XMLElement) elem - The challenge stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_challenge2_cb: function (elem) {
            // remove unneeded handlers
            this.deleteHandler(this._sasl_success_handler);
            this.deleteHandler(this._sasl_failure_handler);

            this._sasl_success_handler = this._addSysHandler(
                this._sasl_success_cb.bind(this), null,
                "success", null, null);
            this._sasl_failure_handler = this._addSysHandler(
                this._sasl_failure_cb.bind(this), null,
                "failure", null, null);
            this.send($build('response', {xmlns: Strophe.NS.SASL}).tree());
            return false;
        },

        /** PrivateFunction: _auth1_cb
         *  _Private_ handler for legacy authentication.
         *
         *  This handler is called in response to the initial <iq type='get'/>
         *  for legacy authentication.  It builds an authentication <iq/> and
         *  sends it, creating a handler (calling back to _auth2_cb()) to
         *  handle the result
         *
         *  Parameters:
         *    (XMLElement) elem - The stanza that triggered the callback.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _auth1_cb: function (elem) {
            // build plaintext auth iq
            var iq = $iq({type: "set", id: "_auth_2"})
                .c('query', {xmlns: Strophe.NS.AUTH})
                .c('username', {}).t(Strophe.getNodeFromJid(this.jid))
                .up()
                .c('password').t(this.pass);

            if (!Strophe.getResourceFromJid(this.jid)) {
                // since the user has not supplied a resource, we pick
                // a default one here.  unlike other auth methods, the server
                // cannot do this for us.
                this.jid = Strophe.getBareJidFromJid(this.jid) + '/strophe';
            }
            iq.up().c('resource', {}).t(Strophe.getResourceFromJid(this.jid));

            this._addSysHandler(this._auth2_cb.bind(this), null,
                null, null, "_auth_2");

            this.send(iq.tree());

            return false;
        },

        /** PrivateFunction: _sasl_success_cb
         *  _Private_ handler for succesful SASL authentication.
         *
         *  Parameters:
         *    (XMLElement) elem - The matching stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_success_cb: function (elem) {
            Strophe.info("SASL authentication succeeded.");

            // remove old handlers
            this.deleteHandler(this._sasl_failure_handler);
            this._sasl_failure_handler = null;
            if (this._sasl_challenge_handler) {
                this.deleteHandler(this._sasl_challenge_handler);
                this._sasl_challenge_handler = null;
            }

            this._addSysHandler(this._sasl_auth1_cb.bind(this), null,
                "stream:features", null, null);

            // we must send an xmpp:restart now
            this._sendRestart();

            return false;
        },

        /** PrivateFunction: _sasl_auth1_cb
         *  _Private_ handler to start stream binding.
         *
         *  Parameters:
         *    (XMLElement) elem - The matching stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_auth1_cb: function (elem) {
            // save stream:features for future usage
            this.features = elem;

            var i, child;

            for (i = 0; i < elem.childNodes.length; i++) {
                child = elem.childNodes[i];
                if (child.nodeName == 'bind') {
                    this.do_bind = true;
                }

                if (child.nodeName == 'session') {
                    this.do_session = true;
                }
            }

            if (!this.do_bind) {
                this._changeConnectStatus(Strophe.Status.AUTHFAIL, null);
                return false;
            } else {
                this._addSysHandler(this._sasl_bind_cb.bind(this), null, null,
                    null, "_bind_auth_2");

                var resource = Strophe.getResourceFromJid(this.jid);
                if (resource) {
                    this.send($iq({type: "set", id: "_bind_auth_2"})
                        .c('bind', {xmlns: Strophe.NS.BIND})
                        .c('resource', {}).t(resource).tree());
                } else {
                    this.send($iq({type: "set", id: "_bind_auth_2"})
                        .c('bind', {xmlns: Strophe.NS.BIND})
                        .tree());
                }
            }

            return false;
        },

        /** PrivateFunction: _sasl_bind_cb
         *  _Private_ handler for binding result and session start.
         *
         *  Parameters:
         *    (XMLElement) elem - The matching stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_bind_cb: function (elem) {
            if (elem.getAttribute("type") == "error") {
                Strophe.info("SASL binding failed.");
                this._changeConnectStatus(Strophe.Status.AUTHFAIL, null);
                return false;
            }

            // TODO - need to grab errors
            var bind = elem.getElementsByTagName("bind");
            var jidNode;
            if (bind.length > 0) {
                // Grab jid
                jidNode = bind[0].getElementsByTagName("jid");
                if (jidNode.length > 0) {
                    this.jid = Strophe.getText(jidNode[0]);

                    if (this.do_session) {
                        this._addSysHandler(this._sasl_session_cb.bind(this),
                            null, null, null, "_session_auth_2");

                        this.send($iq({type: "set", id: "_session_auth_2"})
                            .c('session', {xmlns: Strophe.NS.SESSION})
                            .tree());
                    } else {
                        this.authenticated = true;
                        this._changeConnectStatus(Strophe.Status.CONNECTED, null);
                    }
                }
            } else {
                Strophe.info("SASL binding failed.");
                this._changeConnectStatus(Strophe.Status.AUTHFAIL, null);
                return false;
            }
        },

        /** PrivateFunction: _sasl_session_cb
         *  _Private_ handler to finish successful SASL connection.
         *
         *  This sets Connection.authenticated to true on success, which
         *  starts the processing of user handlers.
         *
         *  Parameters:
         *    (XMLElement) elem - The matching stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_session_cb: function (elem) {
            if (elem.getAttribute("type") == "result") {
                this.authenticated = true;
                this._changeConnectStatus(Strophe.Status.CONNECTED, null);
            } else if (elem.getAttribute("type") == "error") {
                Strophe.info("Session creation failed.");
                this._changeConnectStatus(Strophe.Status.AUTHFAIL, null);
                return false;
            }

            return false;
        },

        /** PrivateFunction: _sasl_failure_cb
         *  _Private_ handler for SASL authentication failure.
         *
         *  Parameters:
         *    (XMLElement) elem - The matching stanza.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _sasl_failure_cb: function (elem) {
            // delete unneeded handlers
            if (this._sasl_success_handler) {
                this.deleteHandler(this._sasl_success_handler);
                this._sasl_success_handler = null;
            }
            if (this._sasl_challenge_handler) {
                this.deleteHandler(this._sasl_challenge_handler);
                this._sasl_challenge_handler = null;
            }

            this._changeConnectStatus(Strophe.Status.AUTHFAIL, null);
            return false;
        },

        /** PrivateFunction: _auth2_cb
         *  _Private_ handler to finish legacy authentication.
         *
         *  This handler is called when the result from the jabber:iq:auth
         *  <iq/> stanza is returned.
         *
         *  Parameters:
         *    (XMLElement) elem - The stanza that triggered the callback.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _auth2_cb: function (elem) {
            if (elem.getAttribute("type") == "result") {
                this.authenticated = true;
                this._changeConnectStatus(Strophe.Status.CONNECTED, null);
            } else if (elem.getAttribute("type") == "error") {
                this._changeConnectStatus(Strophe.Status.AUTHFAIL, null);
                this.disconnect();
            }

            return false;
        },

        /** PrivateFunction: _addSysTimedHandler
         *  _Private_ function to add a system level timed handler.
         *
         *  This function is used to add a Strophe.TimedHandler for the
         *  library code.  System timed handlers are allowed to run before
         *  authentication is complete.
         *
         *  Parameters:
         *    (Integer) period - The period of the handler.
         *    (Function) handler - The callback function.
         */
        _addSysTimedHandler: function (period, handler) {
            var thand = new Strophe.TimedHandler(period, handler);
            thand.user = false;
            this.addTimeds.push(thand);
            return thand;
        },

        /** PrivateFunction: _addSysHandler
         *  _Private_ function to add a system level stanza handler.
         *
         *  This function is used to add a Strophe.Handler for the
         *  library code.  System stanza handlers are allowed to run before
         *  authentication is complete.
         *
         *  Parameters:
         *    (Function) handler - The callback function.
         *    (String) ns - The namespace to match.
         *    (String) name - The stanza name to match.
         *    (String) type - The stanza type attribute to match.
         *    (String) id - The stanza id attribute to match.
         */
        _addSysHandler: function (handler, ns, name, type, id) {
            var hand = new Strophe.Handler(handler, ns, name, type, id);
            hand.user = false;
            this.addHandlers.push(hand);
            return hand;
        },

        /** PrivateFunction: _onDisconnectTimeout
         *  _Private_ timeout handler for handling non-graceful disconnection.
         *
         *  If the graceful disconnect process does not complete within the
         *  time allotted, this handler finishes the disconnect anyway.
         *
         *  Returns:
         *    false to remove the handler.
         */
        _onDisconnectTimeout: function () {
            Strophe.info("_onDisconnectTimeout was called");

            // cancel all remaining requests and clear the queue
            var req;
            while (this._requests.length > 0) {
                req = this._requests.pop();
                req.abort = true;
                req.xhr.abort();
                // jslint complains, but this is fine. setting to empty func
                // is necessary for IE6
                req.xhr.onreadystatechange = function () {
                };
            }

            // actually disconnect
            this._doDisconnect();

            return false;
        },

        /** PrivateFunction: _onIdle
         *  _Private_ handler to process events during idle cycle.
         *
         *  This handler is called every 100ms to fire timed handlers that
         *  are ready and keep poll requests going.
         */
        _onIdle: function () {
            var i, thand, since, newList;

            // add timed handlers scheduled for addition
            // NOTE: we add before remove in the case a timed handler is
            // added and then deleted before the next _onIdle() call.
            while (this.addTimeds.length > 0) {
                this.timedHandlers.push(this.addTimeds.pop());
            }

            // remove timed handlers that have been scheduled for deletion
            while (this.removeTimeds.length > 0) {
                thand = this.removeTimeds.pop();
                i = this.timedHandlers.indexOf(thand);
                if (i >= 0) {
                    this.timedHandlers.splice(i, 1);
                }
            }

            // call ready timed handlers
            var now = new Date().getTime();
            newList = [];
            for (i = 0; i < this.timedHandlers.length; i++) {
                thand = this.timedHandlers[i];
                if (this.authenticated || !thand.user) {
                    since = thand.lastCalled + thand.period;
                    if (since - now <= 0) {
                        if (thand.run()) {
                            newList.push(thand);
                        }
                    } else {
                        newList.push(thand);
                    }
                }
            }
            this.timedHandlers = newList;

            var body, time_elapsed;

            // if no requests are in progress, poll
            if (this.authenticated && this._requests.length === 0 &&
                this._data.length === 0 && !this.disconnecting) {
                Strophe.info("no requests during idle cycle, sending " +
                    "blank request");
                this._data.push(null);
            }

            if (this._requests.length < 2 && this._data.length > 0 && !this.paused) {
                body = this._buildBody();
                for (i = 0; i < this._data.length; i++) {
                    if (this._data[i] !== null) {
                        if (this._data[i] === "restart") {
                            body.attrs({
                                to: this.domain,
                                "xml:lang": "en",
                                "xmpp:restart": "true",
                                "xmlns:xmpp": Strophe.NS.BOSH
                            });
                        } else {
                            body.cnode(this._data[i]).up();
                        }
                    }
                }
                delete this._data;
                this._data = [];
                this._requests.push(
                    new Strophe.Request(body.tree(),
                        this._onRequestStateChange.bind(
                            this, this._dataRecv.bind(this)),
                        body.tree().getAttribute("rid")));
                this._processRequest(this._requests.length - 1);
            }

            if (this._requests.length > 0) {
                time_elapsed = this._requests[0].age();
                if (this._requests[0].dead !== null) {
                    if (this._requests[0].timeDead() >
                        Math.floor(Strophe.SECONDARY_TIMEOUT * this.wait)) {
                        this._throttledRequestHandler();
                    }
                }

                if (time_elapsed > Math.floor(Strophe.TIMEOUT * this.wait)) {
                    Strophe.warn("Request " +
                        this._requests[0].id +
                        " timed out, over " + Math.floor(Strophe.TIMEOUT * this.wait) +
                        " seconds since last activity");
                    this._throttledRequestHandler();
                }
            }

            clearTimeout(this._idleTimeout);

            // reactivate the timer only if connected
            if (this.connected) {
                this._idleTimeout = setTimeout(this._onIdle.bind(this), 100);
            }
        }
    };

    if (callback) {
        callback(Strophe, $build, $msg, $iq, $pres);
    }

})(function () {
    window.Strophe = arguments[0];
    window.$build = arguments[1];
    window.$msg = arguments[2];
    window.$iq = arguments[3];
    window.$pres = arguments[4];
});

// http://xmpp.org/extensions/xep-0059.html

Strophe.addNamespace('RSM', 'http://jabber.org/protocol/rsm');

Strophe.RSM = function (options) {
    this.attribs = ['max', 'first', 'last', 'after', 'before', 'index', 'count'];

    if (typeof options.xml != 'undefined') {
        this.fromXMLElement(options.xml);
    } else {
        for (var ii = 0; ii < this.attribs.length; ii++) {
            var attrib = this.attribs[ii];
            this[attrib] = options[attrib];
        }
    }
};

Strophe.RSM.prototype = {
    toXML: function () {
        var xml = $build('set', {xmlns: Strophe.NS.RSM});
        for (var ii = 0; ii < this.attribs.length; ii++) {
            var attrib = this.attribs[ii];
            if (typeof this[attrib] != 'undefined') {
                xml = xml.c(attrib).t(this[attrib].toString()).up();
            }
        }
        return xml.tree();
    },

    next: function (max) {
        var newSet = new Strophe.RSM({max: max, after: this.last});
        return newSet;
    },

    previous: function (max) {
        var newSet = new Strophe.RSM({max: max, before: this.first});
        return newSet;
    },

    fromXMLElement: function (xmlElement) {
        for (var ii = 0; ii < this.attribs.length; ii++) {
            var attrib = this.attribs[ii];
            var elem = xmlElement.getElementsByTagName(attrib)[0];
            if (typeof elem != 'undefined' && elem !== null) {
                this[attrib] = Strophe.getText(elem);
                if (attrib == 'first') {
                    this.index = elem.getAttribute('index');
                }
            }
        }
    }
};

/**
 * Chat state notifications (XEP 0085) plugin
 * @see http://xmpp.org/extensions/xep-0085.html
 */
Strophe.addConnectionPlugin('chatstates',
    {
        init: function (connection) {
            this._connection = connection;

            Strophe.addNamespace('CHATSTATES', 'http://jabber.org/protocol/chatstates');
        },

        statusChanged: function (status) {
            if (status === Strophe.Status.CONNECTED
                || status === Strophe.Status.ATTACHED) {
                this._connection.addHandler(this._notificationReceived.bind(this),
                    Strophe.NS.CHATSTATES, "message");
            }
        },

        addActive: function (message) {
            return message.c('active', {xmlns: Strophe.NS.CHATSTATES}).up();
        },

        _notificationReceived: function (message) {
            var composing = $(message).find('composing'),
                paused = $(message).find('paused'),
                active = $(message).find('active'),
                jid = $(message).attr('from');

            if (composing.length > 0) {
                $(document).trigger('composing.chatstates', jid);
            }

            if (paused.length > 0) {
                $(document).trigger('paused.chatstates', jid);
            }

            if (active.length > 0) {
                $(document).trigger('active.chatstates', jid);
            }

            return true;
        },

        sendActive: function (jid, type) {
            this._sendNotification(jid, type, 'active');
        },

        sendComposing: function (jid, type) {
            this._sendNotification(jid, type, 'composing');
        },

        sendPaused: function (jid, type) {
            this._sendNotification(jid, type, 'paused');
        },

        _sendNotification: function (jid, type, notification) {
            if (!type) type = 'chat';

            this._connection.send($msg(
                {
                    to: jid,
                    type: type
                })
                .c(notification, {xmlns: Strophe.NS.CHATSTATES}));
        }
    });

// http://xmpp.org/extensions/xep-0136.html
Strophe.addConnectionPlugin('archive', {
    _connection: null,

    init: function (connection) {
        this._connection = connection;
        Strophe.addNamespace('DELAY', 'jabber:x:delay');
        Strophe.addNamespace('ARCHIVE', 'urn:xmpp:archive');
    },

    listCollections: function (jid, rsm, callback) {
        var xml = $iq({type: 'get', id: this._connection.getUniqueId('list')}).c('list', {xmlns: Strophe.NS.ARCHIVE, 'with': jid});
        if (rsm) {
            xml = xml.cnode(rsm.toXML());
        }
        this._connection.sendIQ(xml, this._handleListConnectionResponse.bind(this, callback));
    },

    retrieveMessages: function (jid, rsm, callback) {
        new Strophe.ArchivedCollection(this._connection, jid).retrieveMessages(rsm, callback);
    },

    _handleListConnectionResponse: function (callback, stanza) {
        var collections = [];
        var chats = stanza.getElementsByTagName('chat');
        for (var ii = 0; ii < chats.length; ii++) {
            var jid = chats[ii].getAttribute('with');
            var start = chats[ii].getAttribute('start');
            collections.push(new Strophe.ArchivedCollection(this._connection, jid, start));
        }
        var responseRsm = new Strophe.RSM({xml: stanza.getElementsByTagName('set')[0]});
        callback(collections, responseRsm);
    }
});

Strophe.ArchivedCollection = function (connection, jid) {
    this.connection = connection;
    this.jid = jid;
//  this.start = start;
//  this.startDate = (new Date()).setISO8601(start);
};

Strophe.ArchivedCollection.prototype = {
    retrieveMessages: function (rsm, callback) {
        var builder = $iq({type: 'get', id: this.connection.getUniqueId('retrieve')}).c('retrieve', {xmlns: Strophe.NS.ARCHIVE, 'with': this.jid/*, start: this.start*/});
        if (rsm) {
            builder = builder.cnode(rsm.toXML());
        }
        this.connection.sendIQ(builder, function (stanza) {
            var messages = [];
            var myJid = Strophe.getBareJidFromJid(this.connection.jid);
            var responseRsm;
            var msgTimestamp;
            var chat = stanza.getElementsByTagName('chat')[0];
            var timestamp = (new Date()).setISO8601(chat.getAttribute("start"));
            var element = chat.firstChild;
            while (element) {
                switch (element.tagName) {
                    case 'to':
                        msgTimestamp = this._incrementTimestampForMessage(timestamp, element);
                        messages.push(new Strophe.ArchivedMessage(msgTimestamp, myJid, this.jid, Strophe.getText(element.getElementsByTagName('body')[0]), Boolean(parseInt(element.getAttribute("isRead")))));
                        break;
                    case 'from':
                        msgTimestamp = this._incrementTimestampForMessage(timestamp, element);
                        messages.push(new Strophe.ArchivedMessage(msgTimestamp, this.jid, myJid, Strophe.getText(element.getElementsByTagName('body')[0]), Boolean(parseInt(element.getAttribute("isRead")))));
                        break;
                    case 'set':
                        responseRsm = new Strophe.RSM({xml: element});
                        break;
                    default:
                        break;
                }
                element = element.nextSibling;
            }
            callback(messages, responseRsm);
        }.bind(this));
    },

    _incrementTimestampForMessage: function (timestamp, element) {
        var secs = element.getAttribute('secs');
        var newTimestamp = new Date('Y-m-d HH:mm:ss');
        newTimestamp.setTime(timestamp.getTime() + Number(secs) * 1000);
        return newTimestamp;
    }
};

Strophe.ArchivedMessage = function (timestamp, from, to, body, isRead) {
    this.timestamp = timestamp;
    this.from = from;
    this.to = to;
    this.body = body;
    this.isRead = isRead
};

Strophe.ArchivedMessage.prototype = {
};


//    XMPP plugins for Strophe v0.2

//    (c) 2012 Yiorgis Gozadinos.
//    strophe.plugins is distributed under the MIT license.
//    http://github.com/ggozad/strophe.plugins


// Roster plugin partially implementing
// [Roster management](http://xmpp.org/rfcs/rfc6121.html) & [Roster Item Exchange](http://xmpp.org/extensions/xep-0144.html)

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery', 'underscore', 'backbone', 'strophe'], function ($, _, Backbone, Strophe) {
            // Also create a global in case some scripts
            // that are loaded still are looking for
            // a global even when an AMD loader is in use.
            return factory($, _, Backbone, Strophe);
        });
    } else {
        // Browser globals
        factory(root.$, root._, root.Backbone, root.Strophe);
    }
}(this, function ($, _, Backbone, Strophe) {

    Strophe.addConnectionPlugin('roster', {
        _connection: null,

        init: function (conn) {
            this._connection = conn;
            Strophe.addNamespace('ROSTERX', 'http://jabber.org/protocol/rosterx');
            _.extend(this, Backbone.Events);
        },

        statusChanged: function (status, condition) {
            if (status === Strophe.Status.CONNECTED || status === Strophe.Status.ATTACHED) {
                // Subscribe to Presence
                this._connection.addHandler(this._onReceivePresence.bind(this), null, 'presence', null, null, null);
                // Subscribe to roster push from the server
                this._connection.addHandler(this._onRosterSet.bind(this), Strophe.NS.ROSTER, 'iq', 'set');
                // Subscribe to Roster Item exchange messages
                this._connection.addHandler(this._onRosterSuggestion.bind(this), Strophe.NS.ROSTERX, 'message', null);
            }
        },

        // **get** resolves with a dictionary of the authenticated user's roster.get:function(){var d=$.Deferred(),roster,iq=$iq({type:'get',id:this._connection.getUniqueId('roster')}).c('query',{xmlns:Strophe.NS.ROSTER});this._connection.sendIQ(iq.tree(),function(result){roster={};$.each($('item',result),function(idx,item){roster[item.getAttribute('jid')]={subscription:item.getAttribute('subscription'),name:item.getAttribute('name'),groups:$.map($('group',item),function(group,idx){return $(group).text();})};});d.resolve(roster);},d.reject);return d.promise();}, subscribe:function(jid){this._connection.send($pres({to:jid,type:"subscribe"}));}, unsubscribe:function(jid){this._connection.send($pres({to:jid,type:"unsubscribe"}));}, authorize:function(jid){this._connection.send($pres({to:jid,type:"subscribed"}));}, unauthorize:function(jid){this._connection.send($pres({to:jid,type:"unsubscribed"}));},update:function(jid,name,groups){var d=$.Deferred(),i,iq=$iq({type:'set',id:this._connection.getUniqueId('roster')}).c('query',{xmlns:Strophe.NS.ROSTER}).c('item',{jid:jid,name:name});for(i=0;i<groups.length;i++){iq.c('group').t(groups[i]).up();}
        this._connection.sendIQ(iq.tree(), d.resolve, d.reject);
    return d.promise();
}, _onReceivePresence
:
function (presence) {
    var jid = presence.getAttribute('from'), type = presence.getAttribute('type'), show = (presence.getElementsByTagName('show').length !== 0) ? Strophe.getText(presence.getElementsByTagName('show')[0]) : null, status = (presence.getElementsByTagName('status').length !== 0) ? Strophe.getText(presence.getElementsByTagName('status')[0]) : null, priority = (presence.getElementsByTagName('priority').length !== 0) ? Strophe.getText(presence.getElementsByTagName('priority')[0]) : null;
    this.trigger('xmpp:presence', {jid: jid, type: type, show: show, status: status, priority: priority});
    switch (type) {
        case null:
            this.trigger('xmpp:presence:available', {jid: jid, show: show, status: status, priority: priority});
            break;
        case'unavailable':
            this.trigger('xmpp:presence:unavailable', {jid: jid});
            break;
        case'subscribe':
            this.trigger('xmpp:presence:subscriptionrequest', {jid: jid});
            break;
        default:
            break;
    }
    return true;
}
,
_onRosterSet:function (iq) {
    var items = $('item', iq);
    var data = _.map(items, function (item) {
        var ritem = _.reduce(item.attributes, function (memo, attr) {
            memo[attr.name] = attr.value;
            return memo;
        }, {});
        var groups = _.map($('group', item), function (group) {
            return group.textContent;
        });
        if (groups.length) {
            ritem.groups = groups;
        }
        return ritem;
    });
    this.trigger('xmpp:roster:set', data);
    return true;
}
,
_onRosterSuggestion:function (msg) {
    var self = this, from = $(msg).attr('from'), suggestion, groups;
    $.each($('item', msg), function (idx, item) {
        suggestion = {from: from};
        _.each(item.attributes, function (attr) {
            suggestion[attr.name] = attr.value;
        });
        groups = _.map($('groups', item), function (group) {
            return group.textContent;
        });
        if (groups.length) {
            suggestion.groups = groups;
        }
        self.trigger('xmpp:roster:suggestion', suggestion);
        switch (suggestion.action) {
            case'add':
                self.trigger('xmpp:roster:suggestion:add', suggestion);
                break;
            case'delete':
                self.trigger('xmpp:roster:suggestion:delete', suggestion);
                break;
            case'modify':
                self.trigger('xmpp:roster:suggestion:modify', suggestion);
                break;
            default:
                break;
        }
    });
    return true;
}
})
;
}))
;
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery', 'underscore', 'backbone', 'strophe'], function ($, _, Backbone, Strophe) {
            return factory($, _, Backbone, Strophe);
        });
    } else {
        factory(root.$, root._, root.Backbone, root.Strophe);
    }
}(this, function ($, _, Backbone, Strophe) {
    Strophe.addConnectionPlugin('message', {_connection: null, init: function (conn) {
        this._connection = conn;
        Strophe.addNamespace('XHTML_IM', 'http://jabber.org/protocol/xhtml-im');
        Strophe.addNamespace('XHTML', 'http://www.w3.org/1999/xhtml');
        _.extend(this, Backbone.Events);
    }, statusChanged: function (status, condition) {
        if (status === Strophe.Status.CONNECTED || status === Strophe.Status.ATTACHED) {
            this._connection.addHandler(this._onReceiveChatMessage.bind(this), null, 'message', 'chat');
        }
    }, _onReceiveChatMessage: function (message) {
        var body, html_body;
        if ($(message).find("delay")[0]) {
            return true;
        }
        body = $(message).children('body').text();
        if (body === '') {
            return true;
        }
        html_body = $('html[xmlns="' + Strophe.NS.XHTML_IM + '"] > body', message);
        if (html_body.length > 0) {
            html_body = $('<div>').append(html_body.contents()).html();
        } else {
            html_body = null;
        }
        this.trigger('xmpp:message', {jid: message.getAttribute('from'), type: message.getAttribute('type'), body: body, html_body: html_body});
        return true;
    }, send: function (to, body, html_body) {
        var msg = $msg({to: to, type: 'chat'});
        if (body) {
            msg.c('body', {}, body);
        }
        if (html_body) {
            msg.c('html', {xmlns: Strophe.NS.XHTML_IM}).c('body', {xmlns: Strophe.NS.XHTML}).h(html_body);
        }
        this._connection.send(msg.tree());
    }});
}));
var ServerDate = function () {
    if (arguments.length === 0) {
        return new Date(new Date().valueOf() + ServerDate.skew);
    }
    else if (arguments.length === 1) {
        return new Date(arguments[0]);
    }
    else {
        return new Date(Date.UTC.apply(null, arguments) + ((new Date()).getTimezoneOffset() * 60000));
    }
};
ServerDate.parse = Date.parse;
ServerDate.UTC = Date.UTC;
ServerDate.now = function () {
    return(new ServerDate()).valueOf();
};
ServerDate.skew = 0;
ServerDate.prototype.toUTCString = function () {
    var a = function (a) {
        return(a = a + "", a.length == 2) ? a : "0" + a
    };
    return function () {
        var d = [this.getUTCFullYear(), a(this.getUTCMonth() + 1), a(this.getUTCDate())].join("-"), f = [a(this.getUTCHours()), a(this.getUTCMinutes()), a(this.getUTCSeconds())].join(":") + "." + this.getMilliseconds();
        return[d, f].join("T") + "Z"
    }
}
Strophe.addConnectionPlugin('serverdate', {init: function (connection) {
    Strophe.Request.prototype._newXHR = function () {
        var xhr = null;
        if (window.XMLHttpRequest) {
            xhr = new XMLHttpRequest();
            if (xhr.overrideMimeType) {
                xhr.overrideMimeType("text/xml");
            }
        } else if (window.ActiveXObject) {
            xhr = new ActiveXObject("Microsoft.XMLHTTP");
        }
        var handler = this.func.bind(null, this);
        xhr.onreadystatechange = function () {
            if (this.readyState == 2) {
                var header = this.getResponseHeader('Date');
                var server_date = new Date(header);
                if (header && server_date != 'Invalid Date') {
                    system_date = new Date();
                    skew_ms = server_date - system_date;
                    ServerDate.skew = skew_ms;
                }
            }
            handler();
        };
        return xhr;
    };
}});
var $commonData = $("#common-data");
var chatServer = $commonData.data("chat-server")
var chatServerDomain = "@" + $commonData.data("chat-domain")
var myTemplate = {tplContactItem: '<div class="avatar"><img src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>"/></div>' + '<div class="nickname"><%= name %></div>' + '<div class="unread-count"><%=unReadCount%></div>' + '<% if( typeof body != "undefined" ) { %><div class="last-message"><%= body %></div><% } %>', tplChatBox: '<div class="chat-title"><%= name %></div>' + '            <div class="chat-message-container">' + '                <div class="message-list"></div>' + '           <div class="chat-status">对方正在输入...</div>' + '       </div>' + '   <div class="chat-editor">' + '           <textarea type="text" class="chat-input" rows="2" ></textarea>' + '       <button class="btn btn-primary btn-send">发送</button>' + '       </div>', tplMessageItem: '<% if(typeof formattedTime != "undefined"){  %>' + '<div class="message-time-wrapper"><div class="message-time"><span class="time-span left"/><%=formattedTime%><span class="time-span right"/></div></div>' + '<% } %>' + '<a href="<%=profileUrl%>" target="_blank" ><img class="avatar" src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>"></a>' + '<div class="message-content"><div class="message-text"><%=body%></div><div class="message-arrow"></div></div>'}
$(function () {
    $(document).trigger('connect', {jid: $commonData.data("uid") + chatServerDomain, password: $commonData.data("pwd")});
})
$(document).bind('connect', function (ev, data) {
    var conn = new Strophe.Connection(chatServer);
    conn.xmlInput = function (elem) {
        if ($(elem).find("message")[0]) {
            chatApp.debug(elem)
        }
    }
    conn.xmlOutput = function (elem) {
        if ($(elem).find("retrieve")[0]) {
            chatApp.debug(elem)
        }
    }
    conn.connect(data.jid, data.password, function (status) {
        if (status === Strophe.Status.CONNECTED) {
            $(document).trigger('connected');
        } else if (status === Strophe.Status.DISCONNECTED) {
            $(document).trigger('disconnected');
        }
    });
    chatApp.connection = conn;
});
var $chatData = $("#chat-data");
var Contact = Backbone.Model.extend({defaults: {show: "offline", name: "", isTyping: false, unReadCount: 0, current: false, avatarUrl: $chatData.data("default-avatar")
}, initialize: function () {
    this.messages = new MessageCollection();
}, url: $chatData.data("get-user-info-url"), addMessage: function (msg) {
    if (msg.isIn()) {
        var sender = msg.sender
        if (!msg.get("isRead")) {
            if (chatApp.isWindowFocused && sender.get("current")) {
                sender.sendReceivedRecipts();
            } else {
                sender.increaseUnReadCount(1);
            }
        }
    }
    this.messages.add(msg);
}, retrieveMessages: function (before) {
    if (!before) {
        before = "";
    }
    var user = this;
    var max = 5;
    chatApp.connection.archive.retrieveMessages(this.get("jid"), new Strophe.RSM({max: max, before: before}), function (messages) {
        var isRetrieveAgain = messages.length == max;
        messages.reverse()
        _.each(messages, function (oldMsg) {
            var msg = new Message({from: Strophe.getNodeFromJid(oldMsg.from), to: Strophe.getNodeFromJid(oldMsg.to), body: oldMsg.body, timestamp: oldMsg.timestamp})
            if (oldMsg.isRead || msg.sender == chatApp.myProfile) {
                isRetrieveAgain = false;
                return;
            }
            msg.sender && msg.sender.addMessage(msg);
        })
        if (isRetrieveAgain) {
            before = messages[0].timestamp.valueOf();
            user.retrieveMessages(before);
        }
    });
}, increaseUnReadCount: function (num) {
    var unReadCount = this.get("unReadCount");
    this.set("unReadCount", unReadCount + num);
    chatApp.totalUnReadCount += num;
    var $totalUnReadCount = $("#total-unread-count");
    $totalUnReadCount.text(chatApp.totalUnReadCount).show();
    if (!chatApp.unReadMsgInterval) {
        chatApp.unReadMsgInterval = setInterval(function () {
            if (chatApp.totalUnReadCount > 0) {
                $totalUnReadCount.is(":visible") ? $totalUnReadCount.hide() : $totalUnReadCount.show();
            } else {
                $totalUnReadCount.hide();
            }
        }, 1000)
    }
}, clearUnReadCount: function () {
    var unReadCount = this.get("unReadCount");
    if (unReadCount) {
        this.sendReceivedRecipts();
        this.set("unReadCount", 0);
        chatApp.totalUnReadCount -= unReadCount;
        $("#total-unread-count").text(chatApp.totalUnReadCount)
        if (chatApp.totalUnReadCount == 0) {
            $("#total-unread-count").hide();
        }
    }
}, sendReceivedRecipts: function () {
    var out = $msg({to: this.get("jid")}).c("received", {'xmlns': "urn:xmpp:receipts", 'id': 1});
    chatApp.connection.send(out);
}});
var ContactCollection = Backbone.Collection.extend({model: Contact, url: $chatData.data("get-user-info-url"), getCurrentUser: function () {
    return this.findWhere({current: true});
}});
var ContactItemView = Backbone.View.extend({tagName: "div", className: "contact-item", id: function () {
    return"contact-" + this.model.id;
}, template: _.template(myTemplate.tplContactItem), initialize: function () {
    this.listenTo(this.model, "change", this.render);
    this.listenTo(this.model.messages, "add", this.render);
    this.listenTo(this.model, "destory", this.close);
}, close: function () {
    this.$el.unbind();
    this.$el.remove();
}, render: function () {
    var messages = this.model.messages, lastMsg, lastMsgJson;
    if (messages.length) {
        lastMsg = messages.last()
        lastMsgJson = {"body": lastMsg.get("body").slice(0, 20), "timestamp": lastMsg.get("timestamp").getTime()}
    } else {
        lastMsgJson = {}
    }
    this.$el.html(this.template(_.extend({}, this.model.attributes, lastMsgJson))).removeClass("online offline").addClass(this.model.get("show"));
    if (this.model.get("current")) {
        this.$el.addClass("current")
    } else {
        this.$el.removeClass("current")
    }
    if (this.model.get("unReadCount") > 0) {
        this.$el.find(".unread-count").show();
    } else {
        this.$el.find(".unread-count").hide();
    }
    return this;
}, events: {"click": "openChat"}, openChat: function (event) {
    var beforeUser = chatApp.contactList.getCurrentUser()
    beforeUser && beforeUser.set("current", false)
    var currentUID = $(event.currentTarget).attr("id").replace("contact-", "")
    var currentUser = chatApp.contactList.get(currentUID)
    currentUser.set("current", true)
    currentUser.clearUnReadCount();
    return false;
}});
var ContactListView = Backbone.View.extend({el: "#roster", initialize: function () {
    this.itemViewList = [];
    this.model.each(function (contact) {
        var contactItemView = new ContactItemView({model: contact});
        this.itemViewList.push(contactItemView);
        this.listenTo(contact.messages, "sort add", function () {
            this.sortContacts()
            this.render();
        })
    }, this)
    this.listenTo(this.model, "change", this.render)
    this.listenTo(this.model, "change:show", function () {
        this.sortContacts()
        this.render()
    })
    this.listenTo(this.model, "add", function (contact) {
        var contactItemView = new ContactItemView({model: contact});
        this.itemViewList.push(contactItemView);
        this.sortContacts()
        this.render()
    });
    this.sortContacts()
    this.render()
}, render: function () {
    _.each(this.itemViewList, function (contactView) {
        this.$el.prepend(contactView.el);
    }, this);
    return this;
}, sortContacts: function () {
    this.itemViewList = _.sortBy(this.itemViewList, function (view) {
        var messages = view.model.messages
        return messages.length ? messages.last().get("timestamp").getTime() : (view.model.get("show") == "online" ? 1 : 0)
    })
}});
var Message = Backbone.Model.extend({defaults: {isRead: false}, initialize: function () {
    this.sender = chatApp.contactList.get(this.get("from")) || chatApp.myProfile
    this.receiver = chatApp.contactList.get(this.get("to")) || chatApp.myProfile
}, isIn: function () {
    return this.get("from") != chatApp.myProfile.id
}
})
var MessageCollection = Backbone.Collection.extend({model: Message, initialize: function () {
    this.on("add", function (msg) {
        var index = this.indexOf(msg), previousMsg, ifShowTime = false;
        if (index > 0) {
            previousMsg = this.at(index - 1);
            (msg.get("timestamp") - previousMsg.get("timestamp")) / 1000 / 60 >= 15 && (ifShowTime = true);
        } else if (index == 0) {
            ifShowTime = true;
        }
        if (ifShowTime) {
            msg.set("formattedTime", this.formatTime(msg.get("timestamp")))
        }
    })
}, comparator: function (msg) {
    return msg.get("timestamp").getTime();
}, formatTime: function (date) {
    var today = new ServerDate()
    var d1, d2, dayGap, resultTime = date.getHourMinuteSecond() + "." + date.getMilliseconds(), resultDate;
    d1 = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    d2 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    dayGap = Math.abs(d1 - d2) / 1000 / 60 / 60 / 24
    if (dayGap == 0) {
        resultDate = ""
    } else if (dayGap == 1) {
        resultDate = "昨天"
    } else if (dayGap == 2) {
        resultDate = "前天"
    } else {
        resultDate = date.getTwoDigitMonth() + "-" + date.getTwoDigitDate()
    }
    return resultDate + " " + resultTime;
}})
var MessageItemView = Backbone.View.extend({tagName: "div", className: "message-item", template: _.template(myTemplate.tplMessageItem), render: function () {
    this.$el.html(this.template(_.extend({}, this.model.attributes, this.model.sender.attributes))).addClass(this.model.isIn() ? "others" : "me")
    return this;
}})
var ChatBoxView = Backbone.View.extend({tagName: "div", className: "chat-box", template: _.template(myTemplate.tplChatBox), initialize: function () {
    this.listenTo(this.model, "change:current change:isTyping change:name", this.render);
    this.listenTo(this.model.messages, "add", function (msg, msgCollection) {
        var msgItemEl = new MessageItemView({model: msg}).render().el
        var index = msgCollection.indexOf(msg)
        if (index == 0) {
            this.$(".message-list").prepend(msgItemEl)
        } else {
            this.$(".message-list .message-item:eq(" + (index - 1) + ")").after(msgItemEl)
        }
        this._scrollChatToBottom()
    });
    this.$el.html(this.template(this.model.attributes));
    this.$("textarea").autosize()
}, render: function () {
    if (this.model.hasChanged("name")) {
        var $mesageList = this.$(".message-list");
        this.$el.html(this.template(this.model.attributes));
        $mesageList[0] && this.$(".message-list").replaceWith($mesageList)
    }
    var show = this.model.get("current");
    if (this.model.hasChanged("current")) {
        if (show) {
            this.$el.show()
            this.$el.find(".chat-input").focus();
        } else {
            this.$el.hide();
        }
        this._scrollChatToBottom()
    }
    show && this.model.get("isTyping") ? this.$el.find(".chat-status").show() : this.$el.find(".chat-status").hide();
    return this;
}, events: {"keypress .chat-input": "keyPressed", "focusout .chat-input": "sendPausedStatus", "click .btn-send": "sendMessage"}, keyPressed: function (ev) {
    if (ev.which === 13) {
        ev.preventDefault();
        this.sendMessage();
        this.sendPausedStatus();
    } else {
        this.sendTypingStatus();
    }
}, sendMessage: function () {
    var $chatInput = this.$el.find(".chat-input");
    var body = $chatInput.val();
    if (!body) {
        return false;
    }
    $chatInput.val("");
    var currentUser = chatApp.contactList.getCurrentUser()
    chatApp.connection.message.send(currentUser.get("jid"), body)
    currentUser.addMessage(new Message({from: chatApp.myProfile.id, to: currentUser.id, body: body, timestamp: new ServerDate()}))
    return false;
}, sendTypingStatus: function () {
    if (!chatApp.myProfile.get("isTyping")) {
        chatApp.connection.chatstates.sendComposing(chatApp.contactList.getCurrentUser().get("jid"), "chat");
        chatApp.myProfile.set("isTyping", true)
    }
    if (chatApp.statesTimeOut) {
        clearTimeout(chatApp.statesTimeOut);
        chatApp.statesTimeOut = null;
    } else {
        chatApp.statesTimeOut = setTimeout(this.sendPausedStatus, 10000);
    }
}, sendPausedStatus: function () {
    if (chatApp.myProfile.get("isTyping")) {
        chatApp.myProfile.set("isTyping", false)
        chatApp.connection.chatstates.sendPaused(chatApp.contactList.getCurrentUser().get("jid"), "chat");
    }
    if (chatApp.statesTimeOut) {
        clearTimeout(chatApp.statesTimeOut);
        chatApp.statesTimeOut = null;
    }
}, _scrollChatToBottom: function () {
    var div = this.$(".message-list")[0];
    div.scrollTop = div.scrollHeight;
}})
var ChatBoxListView = Backbone.View.extend({el: "#chat-right-column", initialize: function () {
    this.listenTo(this.model, "add", function (chat) {
        this.$el.append(new ChatBoxView({model: chat}).render().el);
    }, this);
    this.render()
}, render: function () {
    _.each(this.model.models, function (contact) {
        this.$el.append(new ChatBoxView({model: contact}).render().el);
    }, this);
    return this;
}})
var chatApp = {isVisible: function () {
    return $("#chat-dialog").is(":visible");
}, connection: null, totalUnReadCount: 0, myProfile: new Contact({id: $commonData.data("uid"), avatarUrl: $chatData.data("my-avatar"), profileUrl: $chatData.data("profile-url"), name: $chatData.data("my-name")}), isWindowFocused: false, orignalWindowTitle: $("title").text(), unReadMsgInterval: null, initialize: function () {
}, listContacts: function (roster) {
    var contacts = _.map(roster, function (contact, jid) {
        return new Contact({"id": Strophe.getNodeFromJid(jid), "jid": jid});
    })
    this.contactList = new ContactCollection(contacts);
    this.contactListView = new ContactListView({model: this.contactList})
    this.chatBoxListView = new ChatBoxListView({model: this.contactList})
    contacts.length && this.contactList.fetch({type: 'post', data: {ids: _.pluck(contacts, "id").join(",")}})
    this.contactList.each(function (contact) {
        contact.retrieveMessages();
    })
}, createContact: function (bareJID) {
    var contact = new Contact({"id": Strophe.getNodeFromJid(bareJID), "jid": bareJID});
    contact.fetch({type: 'post', data: {id: contact.id}})
    chatApp.contactList.add(contact);
    return contact;
}, log: function (msg) {
    console && console.log(msg);
}, debug: function (msg) {
    console && console.log(msg);
}}
$(document).bind('connected', function () {
    chatApp.initialize();
    chatApp.connection.roster.get().done(function (roster) {
        chatApp.listContacts(roster)
        chatApp.connection.send($pres());
    })
    $(".btn-follow").live("click", function () {
        chatApp.connection.roster.subscribe($(this).data("uid") + chatServerDomain);
    })
    $(".btn-chat").click(function () {
        var toUID = $(this).data("uid");
        var toJID = toUID + chatServerDomain;
        $("#chat-dialog").modal({show: true})
        if (!chatApp.contactList.get(toUID)) {
            chatApp.createContact(toJID).retrieveMessages();
        }
        chatApp.contactListView.$el.find("#contact-" + toUID).click();
        chatApp.connection.roster.subscribe(toJID);
        return false;
    })
    chatApp.connection.roster.on("xmpp:presence:available",function (data) {
        var contact = chatApp.contactList.get(Strophe.getNodeFromJid(data.jid));
        contact && contact.set('show', "online")
    }).on("xmpp:presence:unavailable",function (data) {
        var contact = chatApp.contactList.get(Strophe.getNodeFromJid(data.jid));
        contact && contact.set('show', "offline")
    }).on("xmpp:presence:subscriptionrequest",function (data) {
        chatApp.connection.roster.authorize(data.jid);
        chatApp.connection.roster.subscribe(data.jid);
    }).on("xmpp:roster:set", function (items) {
        _.each(items, function (item) {
            if (item.subscription != 'remove' && !chatApp.contactList.get(Strophe.getNodeFromJid(item.jid))) {
                chatApp.createContact(item.jid).retrieveMessages();
            }
        });
    })
    chatApp.connection.message.on("xmpp:message", function (data) {
        var fromUID = Strophe.getNodeFromJid(data.jid);
        if (fromUID != chatApp.myProfile.id) {
            var msg = new Message({from: fromUID, to: chatApp.myProfile.id, body: data.body, timestamp: new ServerDate()})
            msg.sender && msg.sender.addMessage(msg);
        }
    });
    $(document).bind("composing.chatstates",function (ev, jid) {
        var contact = chatApp.contactList.get(Strophe.getNodeFromJid(jid));
        contact && contact.set("isTyping", true)
    }).bind("paused.chatstates", function (ev, jid) {
        var contact = chatApp.contactList.get(Strophe.getNodeFromJid(jid));
        contact && contact.set("isTyping", false)
    })
});
$(window).bind("beforeunload", function () {
    chatApp.connection.disconnect();
    chatApp.connection = null;
});
$(window).focus(function () {
    chatApp.isWindowFocused = true;
    if (chatApp.isVisible() && chatApp.contactList.getCurrentUser() && chatApp.contactList.getCurrentUser().get("unReadCount") > 0) {
        chatApp.contactListView.$el.find(".current").click();
    }
}).blur(function () {
    chatApp.isWindowFocused = false;
})
$(document).bind('disconnected', function () {
    chatApp.log("dis-connected");
});
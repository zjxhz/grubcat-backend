(function(a, d) {
    a.htmlEncode = function(b) {
        return b && b.replace ? b.replace(/&/g, "&amp;").replace(/\"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\'/g, "&#39;") : b
    };
    a.htmlDecode = function(b) {
        return b && b.replace ? b.replace(/&nbsp;/gi, " ").replace(/&lt;/gi, "<").replace(/&gt;/gi, ">").replace(/&quot;/gi, '"').replace(/&#39;/gi, "'").replace(/&amp;/gi, "&") : b
    };
    a.hrefEncode = function(b) {
        return"zh_CN" == document.lang ? b.replace(/(((http|https|ftp):\/\/)|www\.)[-\w.]+(:\d+)?(\/([\w\/_=.%-~]*(\?[^\s\u4e00-\u9fa5]+)?)?)?(#[\d\w_-]+)?/ig, function(b) {
            var c = WebMM.model("account");
            return'<a target="_blank" href="' + ("/cgi-bin/mmwebwx-bin/webwxcheckurl?uin=" + c.getUin() + "&sid=" + encodeURIComponent(c.getSid()) + "&skey=" + encodeURIComponent(c.getSkey()) + "&deviceid=" + encodeURIComponent(WebMM.getDeviceId()) + "&opcode=2&requrl=" + (0 == b.indexOf("http") ? "" : "http://") + a.clearHtmlStr(b) + "&scene=1&username=" + c.getUserName()) + '">' + b + "</a>"
        }) : b.replace(/(((http|https|ftp):\/\/)|www\.)[-\w.]+(:\d+)?(\/([\w\/_=.%-~]*(\?[^\s\u4e00-\u9fa5]+)?)?)?(#[\d\w_-]+)?/ig, function(b) {
            return'<a target="_blank" href="' + (0 == b.indexOf("http") ? "" : "http://") + a.clearHtmlStr(b) + '">' + b + "</a>"
        })
    };
    a.isUrl = function(b) {
        return/(((http|https|ftp):\/\/)|www\.)[-\w.]+(:\d+)?(\/([\w\/_=.%-~]*(\?[^\s\u4e00-\u9fa5]+)?)?)?(#[\d\w_-]+)?/ig.test(b)
    };
    a.regFilter = function() {
        var b = /([\^\.\[\$\(\)\|\*\+\?\{\\])/ig;
        return function(a) {
            return a.replace(b, "\\$1")
        }
    }();
    a.getAsciiStr = function(b) {
        return(b || "").replace(/\W/g, "")
    };
    a.clearHtmlStr = function(b) {
        return b ? b.replace(/<[^>]*>/g, "") : b
    };
    a.clearLinkTag = function(b) {
        return b ? b.replace(/<a[^>]*>/g, "") : b
    };
    a.formatNum = function(b, a) {
        var c = (isNaN(b) ? 0 : b).toString(), e = a - c.length;
        return 0 < e ? [Array(e + 1).join("0"), c].join("") : c
    };
    a.numToStr = function(b, a) {
        for(var c = "" + b.toFixed(a), e = /(-?\d+)(\d{3})/;e.test(c);) {
            c = c.replace(e, "$1,$2")
        }
        return c
    };
    a.numToTimeStr = function(b, c) {
        return a.tmpl(c, {SS:a.formatNum(parseInt(b) % 60, 2), MM:a.formatNum(parseInt(b / 60) % 60, 2), HH:a.formatNum(parseInt(b / 3600) % 60, 2)})
    };
    a.formatDate = function(b, c) {
        var e = b instanceof Date ? b : new Date(b), d = a.formatNum;
        return c.replace(/YYYY/g, d(e.getFullYear(), 4)).replace(/MM/g, d(e.getMonth() + 1, 2)).replace(/DD/g, d(e.getDate(), 2)).replace(/hh/g, d(e.getHours(), 2)).replace(/mm/g, d(e.getMinutes(), 2)).replace(/ss/g, d(e.getSeconds(), 2))
    };
    a.endsWith = function(b, a) {
        return-1 !== b.indexOf(a, b.length - a.length)
    };
    a.getAsiiStrLen = function(b) {
        return(b || "").replace(/[^\x00-\xFF]/g, "aa").length
    };
    a.stripStr = function(b, a) {
        var c = 0, e, d;
        e = 0;
        for(d = b.length;e < d && c < a;e++) {
            128 > b.charCodeAt(e) ? c++ : c += 2
        }
        return b.substr(0, e)
    };
    a.subAsiiStr = function(b, c, e, d) {
        for(var f = function(b) {
            return b
        }, l = d ? htmlEncode : f, b = (d ? htmlDecode : f)(a.trim((b || "").toString())), e = e || "", d = Math.max(c - e.length, 1), f = b.length, k = 0, m = -1, n, q = 0;q < f;q++) {
            if(n = b.charCodeAt(q), k += 35 == n || 87 == n ? 1.2 : 255 < n ? 1.5 : 1, -1 == m && k > d && (m = q), k > c) {
                return l(b.substr(0, m)) + e
            }
        }
        return l(b)
    };
    a.parseURLParam = function(b) {
        var c = b.indexOf("?"), b = -1 < c ? b.slice(c + 1) : "", e = {};
        b && a(b.split("&")).each(function(b, a) {
            var c = a.split("=");
            2 == c.length && (e[c[0]] = c[1])
        });
        return e
    };
    a.isArr = Array.isArray || function(b) {
        return"[object Array]" == Object.prototype.toString.call(b)
    };
    a.isObj = function(b) {
        return"object" === typeof b
    };
    var f = 0, c = document.title;
    a.flashTitle = function(b) {
        d.qplus && d.qplus.window.flashWindow && qplus.window.flashWindow();
        clearInterval(f);
        document.title = b;
        f = setInterval(function() {
            document.title = document.title == c ? b : c
        }, 1500)
    };
    a.stopFlashTitle = function() {
        clearInterval(f);
        setTimeout(function() {
            document.title = c
        }, 1E3)
    };
    a.form = function(b, c) {
        var e = c || {}, d = a(document.createElement("form"));
        d.attr("method", "post").attr("action", b);
        for(var f in e) {
            d.append('<input type="hidden" name="' + f + '" value="' + e[f] + '">')
        }
        document.body.appendChild(d[0]);
        d.submit()
    };
    a.fn.getFormParam = function() {
        var b = this, a = {};
        b.size() && ["input", "textarea", "select"].forEach(function(c) {
            b.find(c).forEach(function(b) {
                if(b.name && ("radio" != b.type && "checkbox" != b.type || b.checked)) {
                    a[b.name] = (b.value || "").trim()
                }
            })
        });
        return a
    };
    a.extend2 = function() {
        for(var b = {}, c = 0, e = arguments.length;c < e;c++) {
            a.extend(b, arguments[c])
        }
        return b
    };
    a.safe = function(b, c, a) {
        try {
            return b && b.apply(a || this, c || []), 0
        }catch(e) {
            return Log.e("JS Function: $.safe, e.stack: " + e.stack), -1
        }
    };
    a.getCookie = function(b) {
        return RegExp(["(?:; )?", a.regFilter(b), "=([^;]*);?"].join("")).test(document.cookie) && decodeURIComponent(RegExp.$1)
    };
    a.fn.insertTextToInput = function(b) {
        var c = this[0];
        if(document.selection) {
            c.focus(), document.selection.createRange().text = b
        }else {
            if("number" == typeof c.selectionStart) {
                var a = c.selectionStart, e = c.value;
                c.value = e.substr(0, c.selectionStart) + b + e.substr(c.selectionEnd);
                c.selectionStart = c.selectionEnd = a + b.length
            }else {
                c.value += b
            }
        }
        return this
    };
    a.clone = function(b) {
        return a.extend(!0, {}, {v:b}).v
    };
    a.getExt = function(b) {
        return b.substr(b.lastIndexOf(".") + 1).toLowerCase()
    };
    a.getFileName = function(b) {
        b = a.trim(b).split("\\");
        return b[b.length - 1]
    };
    var e = {".bmp":1, ".png":1, ".jpeg":1, ".jpg":1, ".gif":2};
    a.isImg = function(b) {
        b = a.trim(b) || "";
        b = b.substr(b.lastIndexOf(".")).toLowerCase();
        return!!e[b]
    };
    a.isGif = function() {
        return!1
    };
    a.getSizeDesc = function(b) {
        if(a.isNumeric(b)) {
            return 0 < b >> 20 ? "" + Math.round(10 * b / 1048576) / 10 + "MB" : 0 < b >> 9 ? "" + Math.round(10 * b / 1024) / 10 + "KB" : "" + b + "B"
        }
    };
    a.computeVoiceNodeWidth = function(b) {
        return 2E3 > b ? 80 : 1E4 > b ? 80 + 10 * (b - 2E3) / 1E3 : 6E4 > b ? 160 + 10 * (b - 1E4) / 1E4 : 220
    };
    a.fn.isShow = function() {
        return 0 < this.length && "none" != this.css("display")
    };
    a.canPlayH264 = !!document.createElement("video").canPlayType;
    a.fn.insertTextToInput = function(b) {
        var c = this[0];
        if(!c || "TEXTAREA" != c.tagName && "INPUT" != c.tagName) {
            return this
        }
        if(document.selection) {
            c.focus(), document.selection.createRange().text = b
        }else {
            if("number" == typeof c.selectionStart) {
                var a = c.selectionStart, e = c.value;
                c.value = e.substr(0, c.selectionStart) + b + e.substr(c.selectionEnd);
                c.selectionStart = c.selectionEnd = a + b.length
            }else {
                c.value += b
            }
        }
        return this
    };
    a.fn.moveToInputEnd = function() {
        var b = this[0];
        if(!b || "TEXTAREA" != b.tagName && "INPUT" != b.tagName) {
            return this
        }
        b.focus();
        var c = b.value.length;
        document.selection ? (b = b.createTextRange(), b.moveStart("character", c), b.collapse(), b.select()) : "number" == typeof b.selectionStart && (b.selectionStart = b.selectionEnd = c);
        return this
    };
    a.fn.setDblClickNoSel = function() {
        function b() {
            return(_aoDomObj.getAttribute(c) || "").toString().split(",")
        }
        var c = "__MoUSeDoWnnoSEL__";
        _aoDomObj = this[0];
        1 == b().length && (_aoDomObj.setAttribute(c, [0, "up"]), this.bind("mousedown", function(e) {
            var d = a.now(), f = parseInt(b()[0]);
            _aoDomObj.setAttribute(c, [d, "down"]);
            500 > d - f && e.preventDefault()
        }), this.bind("mouseup", function() {
            var a = b()[0];
            _aoDomObj.setAttribute(c, [a, "up"])
        }), this.bind("selectstart", function(c) {
            "up" == b().pop() && c.preventDefault()
        }));
        return this
    };
    a.isiOS = function() {
        var b = navigator.platform;
        return"iPad" === b || "iPhone" === b || "iPod" === b
    };
    a.isChrome = function() {
        var b = navigator.userAgent.toLowerCase(), c = navigator.appVersion.toLowerCase(), a = -1 < b.indexOf("applewebkit"), c = a ? -1 != c.indexOf("qqbrowser") ? 1 : 0 : 0;
        return a && !c && -1 < b.indexOf("chrome") && 0 > b.indexOf("se 2.x metasr 1.0")
    };
    a.evalVal = function(b) {
        var c = "a" + a.now();
        a.globalEval(["(function(){try{window.", c, "=", b, ";}catch(_oError){}})();"].join(""));
        b = d[c];
        d[c] = null;
        return b
    };
    a.genImgCentralStyle = function(b) {
        var c = a(b), e = b.width, b = b.height, d = c.parent().width(), f = c.parent().height();
        debug("width:" + e + ", height:" + b);
        var l = e / b;
        l > d / f ? (b = f, e = l * b, c.css({height:b, width:e, top:0, left:(d - e) / 2, visibility:"inherit"}).show()) : (e = d, b = e / l, c.css({height:b, width:e, top:(f - b) / 2, left:0, visibility:"inherit"}).show())
    };
    a.transform = function(b, c, a) {
        var e = c.position();
        b.animate({left:e.left, top:e.top, width:c.width(), height:c.height()}, a)
    };
    a.selectText = function(b, c, a) {
        c = c || 0;
        a = a || b.value.length;
        if(b.createTextRange) {
            var e = b.value.length, b = b.createTextRange();
            b.moveStart("character", c);
            b.moveEnd("character", a - e);
            b.select()
        }else {
            b.setSelectionRange(c, a), b.focus()
        }
    };
    a.setInputLength = function(b, c) {
        b.off("keydown").on("keydown", function(b) {
            b = b.keyCode;
            if(a.getAsiiStrLen(this.value) >= c && 8 != b && 37 != b && 39 != b) {
                return!1
            }
        });
        return b
    };
    a.getURLFromFile = function(b) {
        var c = b.name || b.fileName || "";
        if(".gif" == c.substr(c.lastIndexOf(".")).toLowerCase()) {
            return null
        }
        c = null;
        void 0 != window.createObjectURL ? c = window.createObjectURL(b) : void 0 != window.URL ? c = window.URL.createObjectURL(b) : void 0 != window.webkitURL && (c = window.webkitURL.createObjectURL(b));
        return c
    }
})(jQuery, this);
(function() {
    Array.prototype.every || (Array.prototype.every = function(a, d) {
        if(void 0 === this || null === this) {
            throw new TypeError;
        }
        var f = Object(this), c = f.length >>> 0;
        if("function" !== typeof a) {
            throw new TypeError;
        }
        for(var e = 0;e < c;e++) {
            if(e in f && !a.call(d, f[e], e, f)) {
                return!1
            }
        }
        return!0
    });
    Array.prototype.filter || (Array.prototype.filter = function(a, d) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var f = Object(this), c = f.length >>> 0;
        if(typeof a !== "function") {
            throw new TypeError;
        }
        for(var e = [], b = 0;b < c;b++) {
            if(b in f) {
                var h = f[b];
                a.call(d, h, b, f) && e.push(h)
            }
        }
        return e
    });
    Array.prototype.forEach || (Array.prototype.forEach = function(a, d) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var f = Object(this), c = f.length >>> 0;
        if(typeof a !== "function") {
            throw new TypeError;
        }
        for(var e = 0;e < c;e++) {
            e in f && a.call(d, f[e], e, f)
        }
    });
    Array.prototype.indexOf || (Array.prototype.indexOf = function(a) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var d = Object(this), f = d.length >>> 0;
        if(f === 0) {
            return-1
        }
        var c = 0;
        if(arguments.length > 0) {
            c = Number(arguments[1]);
            c !== c ? c = 0 : c !== 0 && (c !== Infinity && c !== -Infinity) && (c = (c > 0 || -1) * Math.floor(Math.abs(c)))
        }
        if(c >= f) {
            return-1
        }
        for(c = c >= 0 ? c : Math.max(f - Math.abs(c), 0);c < f;c++) {
            if(c in d && d[c] === a) {
                return c
            }
        }
        return-1
    });
    Array.isArray = Array.isArray || function(a) {
        return Object.prototype.toString.call(a) === "[object Array]"
    };
    Array.prototype.lastIndexOf || (Array.prototype.lastIndexOf = function(a) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var d = Object(this), f = d.length >>> 0;
        if(f === 0) {
            return-1
        }
        var c = f;
        if(arguments.length > 1) {
            c = Number(arguments[1]);
            c !== c ? c = 0 : c !== 0 && (c !== Infinity && c !== -Infinity) && (c = (c > 0 || -1) * Math.floor(Math.abs(c)))
        }
        for(f = c >= 0 ? Math.min(c, f - 1) : f - Math.abs(c);f >= 0;f--) {
            if(f in d && d[f] === a) {
                return f
            }
        }
        return-1
    });
    Array.prototype.map || (Array.prototype.map = function(a, d) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var f = Object(this), c = f.length >>> 0;
        if(typeof a !== "function") {
            throw new TypeError;
        }
        for(var e = Array(c), b = 0;b < c;b++) {
            b in f && (e[b] = a.call(d, f[b], b, f))
        }
        return e
    });
    Array.prototype.reduce || (Array.prototype.reduce = function(a) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var d = Object(this), f = d.length >>> 0;
        if(typeof a !== "function") {
            throw new TypeError;
        }
        if(f == 0 && arguments.length == 1) {
            throw new TypeError;
        }
        var c = 0, e;
        if(arguments.length >= 2) {
            e = arguments[1]
        }else {
            do {
                if(c in d) {
                    e = d[c++];
                    break
                }
                if(++c >= f) {
                    throw new TypeError;
                }
            }while(1)
        }
        for(;c < f;) {
            c in d && (e = a.call(void 0, e, d[c], c, d));
            c++
        }
        return e
    });
    Array.prototype.reduceRight || (Array.prototype.reduceRight = function(a) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var d = Object(this), f = d.length >>> 0;
        if(typeof a !== "function") {
            throw new TypeError;
        }
        if(f === 0 && arguments.length === 1) {
            throw new TypeError;
        }
        var f = f - 1, c;
        if(arguments.length >= 2) {
            c = arguments[1]
        }else {
            do {
                if(f in this) {
                    c = this[f--];
                    break
                }
                if(--f < 0) {
                    throw new TypeError;
                }
            }while(1)
        }
        for(;f >= 0;) {
            f in d && (c = a.call(void 0, c, d[f], f, d));
            f--
        }
        return c
    });
    Array.prototype.some || (Array.prototype.some = function(a, d) {
        if(this === void 0 || this === null) {
            throw new TypeError;
        }
        var f = Object(this), c = f.length >>> 0;
        if(typeof a !== "function") {
            throw new TypeError;
        }
        for(var e = 0;e < c;e++) {
            if(e in f && a.call(d, f[e], e, f)) {
                return true
            }
        }
        return false
    });
    Date.now || (Date.now = function() {
        return+new Date
    });
    Date.prototype.toJSON || (Date.prototype.toJSON = function() {
        if(typeof this.toISOString !== "function") {
            throw new TypeError;
        }
        return this.toISOString()
    });
    Date.prototype.toUTCString || (Date.prototype.toUTCString = function() {
        var a = function(a) {
            return(a = a + "", a.length == 2) ? a : "0" + a
        };
        return function() {
            var d = [this.getUTCFullYear(), a(this.getUTCMonth() + 1), a(this.getUTCDate())].join("-"), f = [a(this.getUTCHours()), a(this.getUTCMinutes()), a(this.getUTCSeconds())].join(":") + "." + this.getMilliseconds();
            return[d, f].join("T") + "Z"
        }
    }());
    Function.prototype.bind || (Function.prototype.bind = function(a) {
        var d = [].slice, f = d.call(arguments, 1), c = this, e = function() {
        }, b = function() {
            return c.apply(this instanceof e ? this : a || {}, f.concat(d.call(arguments)))
        };
        e.prototype = c.prototype;
        b.prototype = new e;
        return b
    });
    Object.keys || (Object.keys = function(a) {
        if(a !== Object(a)) {
            throw new TypeError("Object.keys called on non-object");
        }
        var d = [], f;
        for(f in a) {
            Object.prototype.hasOwnProperty.call(a, f) && d.push(f)
        }
        return d
    });
    String.prototype.trim || (String.prototype.trim = function() {
        for(var a = this.replace(/^\s\s*/, ""), d = /\s/, f = a.length;d.test(a.charAt(--f));) {
        }
        return a.slice(0, f + 1)
    });
    String.prototype.endsWith || (String.prototype.endsWith = function(a) {
        return this.indexOf(a, this.length - a.length) !== -1
    });
    String.prototype.format || (String.prototype.format = String.prototype.f = function() {
        for(var a = this, d = arguments.length;d--;) {
            a = a.replace(RegExp("\\{" + d + "\\}", "gm"), arguments[d])
        }
        return a
    })
})();
(function(a, d, f) {
    var c = {};
    a.getTmplStr = function(c) {
        return document.getElementById(c).innerHTML
    };
    a.tmpl = function b(d, g) {
        var i = !/\W/.test(d) ? c[d] = c[d] || b(a.getTmplStr(d)) : new Function("obj", "var p=[],print=function(){p.push.apply(p,arguments);};with(obj){p.push('" + d.replace(/[\r\t\n]/g, " ").split("<#").join("\t").replace(/((^|#>)[^\t]*)'/g, "$1\r").replace(/\t=(.*?)#>/g, "',$1,'").split("\t").join("');").split("#>").join("p.push('").split("\r").join("\\'") + "');}return p.join('');");
        return g != f ? i.call(g, g) : i
    }
})(jQuery, this);
(function(a, d, f) {
    function c(b, c, a) {
        var d, b = b.prototype != f ? b.prototype : b;
        c.exec ? d = function(b) {
            return c.exec(b)
        } : c.call && (d = function(b) {
            return c.call(this, b)
        });
        if(d) {
            var j = [], l;
            for(l in b) {
                d(l) && j.push(e(b, l, a))
            }
            return j
        }
        return e(b, c, a)
    }
    function e(b, c, a) {
        var e = b[c];
        !e && (e = function() {
        });
        return b[c] = a(e, c)
    }
    a.extend(a.aop = {}, {before:function(b, a, e) {
        return c(b, a, function(b) {
            return function() {
                return b.apply(this, e.apply(this, arguments) || arguments)
            }
        })
    }, after:function(b, a, e) {
        return c(b, a, function(b) {
            return function() {
                return e.apply(this, b.apply(this, arguments) || arguments)
            }
        })
    }, around:function(b, a, e) {
        return c(b, a, function(b, c) {
            return function() {
                return e.call(this, arguments, b, c)
            }
        })
    }, exception:function(b, a, e) {
        return c(b, a, function(b) {
            return function() {
                try {
                    return b.apply(this, arguments)
                }catch(c) {
                    e.apply(this, [c])
                }
            }
        })
    }})
})(jQuery, this);
JSON = {};
(function() {
    function a(b) {
        return 10 > b ? "0" + b : b
    }
    function d(b) {
        e.lastIndex = 0;
        return e.test(b) ? '"' + b.replace(e, function(b) {
            var c = g[b];
            return"string" === typeof c ? c : "\\u" + ("0000" + b.charCodeAt(0).toString(16)).slice(-4)
        }) + '"' : '"' + b + '"'
    }
    function f(c, a) {
        var e, g, n, q, p = b, s, o = a[c];
        o && ("object" === typeof o && "function" === typeof o.toJSON) && (o = o.toJSON(c));
        "function" === typeof i && (o = i.call(a, c, o));
        switch(typeof o) {
            case "string":
                return d(o);
            case "number":
                return isFinite(o) ? "" + o : "null";
            case "boolean":
                ;
            case "null":
                return"" + o;
            case "object":
                if(!o) {
                    return"null"
                }
                b += h;
                s = [];
                if("[object Array]" === Object.prototype.toString.apply(o)) {
                    q = o.length;
                    for(e = 0;e < q;e += 1) {
                        s[e] = f(e, o) || "null"
                    }
                    n = 0 === s.length ? "[]" : b ? "[\n" + b + s.join(",\n" + b) + "\n" + p + "]" : "[" + s.join(",") + "]";
                    b = p;
                    return n
                }
                if(i && "object" === typeof i) {
                    q = i.length;
                    for(e = 0;e < q;e += 1) {
                        "string" === typeof i[e] && (g = i[e], (n = f(g, o)) && s.push(d(g) + (b ? ": " : ":") + n))
                    }
                }else {
                    for(g in o) {
                        Object.prototype.hasOwnProperty.call(o, g) && (n = f(g, o)) && s.push(d(g) + (b ? ": " : ":") + n)
                    }
                }
                n = 0 === s.length ? "{}" : b ? "{\n" + b + s.join(",\n" + b) + "\n" + p + "}" : "{" + s.join(",") + "}";
                b = p;
                return n
        }
    }
    "function" !== typeof Date.prototype.toJSON && (Date.prototype.toJSON = function() {
        return isFinite(this.valueOf()) ? this.getUTCFullYear() + "-" + a(this.getUTCMonth() + 1) + "-" + a(this.getUTCDate()) + "T" + a(this.getUTCHours()) + ":" + a(this.getUTCMinutes()) + ":" + a(this.getUTCSeconds()) + "Z" : null
    }, String.prototype.toJSON = Number.prototype.toJSON = Boolean.prototype.toJSON = function() {
        return this.valueOf()
    });
    var c = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, e = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, b, h, g = {"\u0008":"\\b", "\t":"\\t", "\n":"\n", "\u000c":"\\f", "\r":"\r", '"':'\\"', "\\":"\\\\"}, i;
    "function" !== typeof JSON.stringify && (JSON.stringify = function(c, a, e) {
        var d;
        h = b = "";
        if(typeof e === "number") {
            for(d = 0;d < e;d = d + 1) {
                h = h + " "
            }
        }else {
            typeof e === "string" && (h = e)
        }
        if((i = a) && typeof a !== "function" && (typeof a !== "object" || typeof a.length !== "number")) {
            throw Error("JSON.stringify");
        }
        return f("", {"":c})
    });
    "function" !== typeof JSON.parse && (JSON.parse = function(b, a) {
        function e(b, c) {
            var d, h, g = b[c];
            if(g && typeof g === "object") {
                for(d in g) {
                    if(Object.prototype.hasOwnProperty.call(g, d)) {
                        h = e(g, d);
                        h !== void 0 ? g[d] = h : delete g[d]
                    }
                }
            }
            return a.call(b, c, g)
        }
        var d, b = "" + b;
        c.lastIndex = 0;
        c.test(b) && (b = b.replace(c, function(b) {
            return"\\u" + ("0000" + b.charCodeAt(0).toString(16)).slice(-4)
        }));
        if(/^[\],:{}\s]*$/.test(b.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) {
            d = eval("(" + b + ")");
            return typeof a === "function" ? e({"":d}, "") : d
        }
        throw new SyntaxError("JSON.parse");
    })
})();
(function(a, d) {
    function f() {
        return this.__instance__ || (this.__instance__ = new this)
    }
    function c(c) {
        return Class.call(this, c)
    }
    d.Class = function(e) {
        var b = "function" == typeof this ? this : function() {
        }, d = function() {
            function c(b, e) {
                b.Super && c(b.Super, e);
                b.init && b.init.apply(e, a)
            }
            var a = arguments;
            this.Root = b.__base__;
            this.Super = b.prototype;
            c(this, this)
        };
        d.prototype = a.extend2({}, b.prototype || {}, e);
        d.__base__ = b.__base__ || d.prototype;
        d.GetStaticInstance = f;
        d.Inherit = c;
        return d
    }
})(jQuery, this);
(function(a) {
    var d = {}, f = {}, c = function(b, c, e, i) {
        a.ajax(a.extend({url:(0 < b.indexOf("?") ? b + "&" : b + "?") + "r=" + a.now(), data:JSON.stringify(c), type:"post", contentType:"application/json; charset=utf-8", dataType:"json", timeout:3E4, beforeSend:function() {
            return e.onbefore && e.onbefore()
        }, success:function(b) {
            if(!b || "0" == b.retcode || b.BaseResponse && 0 === b.BaseResponse.Ret) {
                e.onsuccess && e.onsuccess(b)
            }else {
                var c = b && b.BaseResponse || {}, b = c.Ret || c.retcode || b && b.retcode || -1;
                (!d.globalExceptionHandler || !d.globalExceptionHandler(b)) && e.onerror && e.onerror(b, c.ErrMsg)
            }
        }, error:function(b, c) {
            e.onerror && e.onerror(c, b.status)
        }, complete:function() {
            e.oncomplete && e.oncomplete()
        }}, i))
    }, e = Class({_mbSending:!1, _moQueue:[], init:function(b, c) {
        this.queueId = b;
        this.options = c
    }, send:function(b, e, g) {
        d && d.wait && returun;
        var i = this, g = g || {};
        !i.queueId || i.options && i.options.noDelay ? c(b, e, g, i.options) : (a.aop.before(g, "oncomplete", function() {
            i._mbSending = !1;
            i._fSend(i._moQueue.shift())
        }), i._moQueue.push({url:b, data:e, callback:g}), 10 < i._moQueue.length && (i._mbSending = !1), i._mbSending || i._fSend(i._moQueue.shift()))
    }, clear:function() {
        this._moQueue = []
    }, _fSend:function(b) {
        b && c(b.url, b.data, b.callback, this.options)
    }});
    a.netQueue = function(b, c) {
        return f[b] || (f[b || "__not_defined__"] = new e(b, c || {}))
    };
    a.netQueueSetting = function(b) {
        a.extend(d, b)
    }
})(jQuery, this);
(function(a, d) {
    function f(b) {
        var b = b.dataTransfer.types, c = !1;
        if(null === b) {
            return!0
        }
        a.each(b, function(b, a) {
            "Files" == a && (c = !0)
        });
        return c
    }
    function c(c) {
        var a = "--" + b + "\r\n", a = a + ("Content-Disposition: form-data; name='upload'; filename='" + c + "'\r\n") + "Content-Type: application/octet-stream\r\n\r\n" + (bin + "\r\n");
        return a += "--" + b + "--"
    }
    function e(b, c, e, d, h) {
        var i = g ? g() : new XMLHttpRequest;
        i.open("POST", b, !0);
        i.onabort = i.onerror = function() {
            c.onerror && c.onerror(i.responseText, i.status, e, h)
        };
        i.onload = function() {
            var b = JSON.parse(i.responseText);
            "0" == b.BaseResponse.Ret ? c.onsuccess && c.onsuccess(e, d, a.extend(b, {LocalId:h}), i.status) : c.onerror && c.onerror(i.responseText, i.status, e, h)
        };
        i.onloadend = function() {
            c.oncomplete && c.oncomplete(h)
        };
        if(i.upload || i) {
            (i.upload || i).onprogress = function(b) {
                c.onprogress && c.onprogress(h, (b.loaded || b.position) / (b.total || b.totalSize))
            }
        }
        return i
    }
    var b = "xxxxxxxxx", h = {ondocover:function() {
    }, ondocleave:function() {
    }, ontargetover:function() {
    }, ontargetdrop:function() {
    }, ontargetleave:function() {
    }}, g = null, i = function() {
    };
    _fDragFileUpload = function(g, l, k, m) {
        i = function(h) {
            var g = e(l(), m, h.toUserName, h.name, h.localId);
            if(d.FormData) {
                var i = new FormData;
                i.append("uploadmediarequest", JSON.stringify({BaseRequest:k(), ClientMediaId:"" + a.now(), TotalLen:h.size, StartPos:0, DataLen:h.size, MediaType:4}));
                i.append("filename", h);
                g.send(i)
            }else {
                if(d.FileReader) {
                    var f = new FileReader;
                    this.loadEnd = function() {
                        var a = f.result;
                        null != g.sendAsBinary ? (g.setRequestHeader("content-type", "multipart/form-data; boundary=" + b), g.sendAsBinary(c(h.name, a))) : (g.setRequestHeader("BASE64", 1), g.setRequestHeader("UP-FILENAME", h.name), g.setRequestHeader("UP-SIZE", h.size), g.setRequestHeader("UP-TYPE", h.type), g.send(a))
                    };
                    this.loadError = function(b) {
                        switch(b.target.error.code) {
                            case b.target.error.NOT_FOUND_ERR:
                                document.getElementById(status).innerHTML = "File not found!";
                                break;
                            case b.target.error.NOT_READABLE_ERR:
                                document.getElementById(status).innerHTML = "File not readable!";
                                break;
                            case b.target.error.ABORT_ERR:
                                break;
                            default:
                                document.getElementById(status).innerHTML = "Read error."
                        }
                    };
                    this.loadProgress = function(b) {
                        b.lengthComputable && (b = Math.round(100 * b.loaded / b.total), document.getElementById(status).innerHTML = "Loaded : " + b + "%")
                    };
                    f.addEventListener ? (f.addEventListener("loadend", this.loadEnd, !1), null != status && (f.addEventListener("error", this.loadError, !1), f.addEventListener("progress", this.loadProgress, !1))) : (f.onloadend = this.loadEnd, null != status && (f.onerror = this.loadError, f.onprogress = this.loadProgress));
                    i = null;
                    h.webkitSlice ? i = h.webkitSlice(0, 1025) : h.mozSlice && (i = h.mozSlice(0, 1025));
                    i ? f.readAsBinaryString(i) : f.readAsBinaryString(h)
                }else {
                    g = new XMLHttpRequest, g.open("POST", targetPHP + "?up=true", !0), g.setRequestHeader("UP-FILENAME", h.name), g.setRequestHeader("UP-SIZE", h.size), g.setRequestHeader("UP-TYPE", h.type), g.send(h), status && (document.getElementById(status).innerHTML = "Loaded : 100%")
                }
            }
        };
        g = document.getElementById(g);
        "draggable" in g && (g.addEventListener("dragover", function(b) {
            b.preventDefault();
            h.ontargetover()
        }, !0), g.addEventListener("drop", function(b) {
            b.preventDefault();
            for(var b = b.dataTransfer.files, c = 0, e = b.length;c < e;c++) {
                var d = b[c], g = h.ontargetdrop(d.name || d.fileName, d.size || d.fileSize, 3145728 < d.size ? "" : a.getURLFromFile(d));
                g && g.localId && (d.localId = g.localId, d.toUserName = g.toUserName, i(d))
            }
            if(!b.length) {
                h.ontargetdrop()
            }
        }, !1), g.addEventListener("dragleave", function() {
            h.ontargetleave()
        }, !1), d.addEventListener("dragover", function(b) {
            b.stopPropagation();
            b.preventDefault();
            if(f(b)) {
                h.ondocover()
            }
        }, !1), d.addEventListener("dragleave", function(b) {
            b.stopPropagation();
            b.preventDefault();
            h.ondocleave()
        }, !1), d.addEventListener("drop", function(b) {
            b.stopPropagation();
            b.preventDefault();
            h.ondocleave()
        }, !1))
    };
    a.setDragFileUploadOption = function(b, c) {
        g = b;
        a.extend(h, c)
    };
    a.dragFileUpload = _fDragFileUpload;
    a.uploadFileByForm = function(b) {
        for(var b = b.target.files, c = 0, e = b.length;c < e;c++) {
            var d = b[c], g = h.ontargetdrop(d.name || d.fileName, d.size || d.fileSize, 3145728 < d.size ? "" : a.getURLFromFile(d));
            d.localId = g.localId;
            d.toUserName = g.toUserName;
            i(d)
        }
    }
})(jQuery, this);
(function(a) {
    a.setCookie = function(d, f, c, e, b, h) {
        d && (document.cookie = a.tmpl(["<#=name#>=<#=value#>; ", !c ? "" : "expires=<#=expires#>; ", "path=<#=path#>; domain=<#=domain#>; ", !h ? "" : "<#=secure#>"].join(""), {name:d, value:(f || "").replace(/%/ig, "%25").replace(/=/ig, "%3D").replace(/;/ig, "%3B"), expires:c && c.toGMTString(), path:e || "/", domain:b || document.domain, secure:h ? "secure" : ""}));
        return this
    };
    a.getCookie = function(d) {
        return RegExp(["(\\b|\\s|^|;)", a.regFilter(d), "=([^;]*);?"].join("")).test(document.cookie) && decodeURIComponent(RegExp.$2) || ""
    };
    a.delCookie = function(a, f, c) {
        return this.setCookie(a, "", new Date(0), f, c)
    }
})(jQuery, this);
(function(a, d, f) {
    var c = "", e = [], b = [];
    a.hashChange = function(b) {
        if(a.isFunction(b)) {
            e.push(b)
        }else {
            for(var b = 0, d = e.length;b < d;b++) {
                e[b](c)
            }
        }
    };
    a.hash = function(e) {
        if(e != f) {
            if((e = e.replace(/^#/, "")) && e != c) {
                b.unshift(c = e), 10 < b.length && b.pop(), a.hashChange()
            }
            return this
        }
        return c
    };
    a.history = a.extend(b, {pushState:function() {
    }, back:function() {
        var b = this.shift();
        c = this[0] || "";
        b != c && a.hashChange()
    }})
})(jQuery, this);
(function(a, d) {
    a.fn.jPlayer = function(c) {
        var e = "string" === typeof c, b = Array.prototype.slice.call(arguments, 1), h = this, c = !e && b.length ? a.extend.apply(null, [!0, c].concat(b)) : c;
        if(e && "_" === c.charAt(0)) {
            return h
        }
        e ? this.each(function() {
            var e = a.data(this, "jPlayer"), i = e && a.isFunction(e[c]) ? e[c].apply(e, b) : e;
            if(i !== e && i !== d) {
                return h = i, !1
            }
        }) : this.each(function() {
            var b = a.data(this, "jPlayer");
            b ? b.option(c || {}) : a.data(this, "jPlayer", new a.jPlayer(c, this))
        });
        return h
    };
    a.jPlayer = function(c, e) {
        if(arguments.length) {
            this.element = a(e);
            this.options = a.extend(!0, {}, this.options, c);
            var b = this;
            this.element.bind("remove.jPlayer", function() {
                b.destroy()
            });
            this._init()
        }
    };
    a.jPlayer.emulateMethods = "load play pause";
    a.jPlayer.emulateStatus = "src readyState networkState currentTime duration paused ended playbackRate";
    a.jPlayer.emulateOptions = "muted volume";
    a.jPlayer.reservedEvent = "ready flashreset resize repeat error warning";
    a.jPlayer.event = {ready:"jPlayer_ready", flashreset:"jPlayer_flashreset", resize:"jPlayer_resize", repeat:"jPlayer_repeat", click:"jPlayer_click", error:"jPlayer_error", warning:"jPlayer_warning", loadstart:"jPlayer_loadstart", progress:"jPlayer_progress", suspend:"jPlayer_suspend", abort:"jPlayer_abort", emptied:"jPlayer_emptied", stalled:"jPlayer_stalled", play:"jPlayer_play", pause:"jPlayer_pause", loadedmetadata:"jPlayer_loadedmetadata", loadeddata:"jPlayer_loadeddata", waiting:"jPlayer_waiting",
        playing:"jPlayer_playing", canplay:"jPlayer_canplay", canplaythrough:"jPlayer_canplaythrough", seeking:"jPlayer_seeking", seeked:"jPlayer_seeked", timeupdate:"jPlayer_timeupdate", ended:"jPlayer_ended", ratechange:"jPlayer_ratechange", durationchange:"jPlayer_durationchange", volumechange:"jPlayer_volumechange"};
    a.jPlayer.htmlEvent = "loadstart abort emptied stalled loadedmetadata loadeddata canplay canplaythrough ratechange".split(" ");
    a.jPlayer.pause = function() {
        a.each(a.jPlayer.prototype.instances, function(c, a) {
            a.data("jPlayer").status.srcSet && a.jPlayer("pause")
        })
    };
    a.jPlayer.timeFormat = {showHour:!1, showMin:!0, showSec:!0, padHour:!1, padMin:!0, padSec:!0, sepHour:":", sepMin:":", sepSec:""};
    a.jPlayer.convertTime = function(c) {
        var e = new Date(1E3 * c), b = e.getUTCHours(), c = e.getUTCMinutes(), e = e.getUTCSeconds(), b = a.jPlayer.timeFormat.padHour && 10 > b ? "0" + b : b, c = a.jPlayer.timeFormat.padMin && 10 > c ? "0" + c : c, e = a.jPlayer.timeFormat.padSec && 10 > e ? "0" + e : e;
        return(a.jPlayer.timeFormat.showHour ? b + a.jPlayer.timeFormat.sepHour : "") + (a.jPlayer.timeFormat.showMin ? c + a.jPlayer.timeFormat.sepMin : "") + (a.jPlayer.timeFormat.showSec ? e + a.jPlayer.timeFormat.sepSec : "")
    };
    a.jPlayer.uaBrowser = function(c) {
        var c = c.toLowerCase(), a = /(opera)(?:.*version)?[ \/]([\w.]+)/, b = /(msie) ([\w.]+)/, d = /(mozilla)(?:.*? rv:([\w.]+))?/, c = /(webkit)[ \/]([\w.]+)/.exec(c) || a.exec(c) || b.exec(c) || 0 > c.indexOf("compatible") && d.exec(c) || [];
        return{browser:c[1] || "", version:c[2] || "0"}
    };
    a.jPlayer.uaPlatform = function(c) {
        var a = c.toLowerCase(), b = /(android)/, d = /(mobile)/, c = /(ipad|iphone|ipod|android|blackberry|playbook|windows ce|webos)/.exec(a) || [], a = /(ipad|playbook)/.exec(a) || !d.exec(a) && b.exec(a) || [];
        c[1] && (c[1] = c[1].replace(/\s/g, "_"));
        return{platform:c[1] || "", tablet:a[1] || ""}
    };
    a.jPlayer.browser = {};
    a.jPlayer.platform = {};
    var f = a.jPlayer.uaBrowser(navigator.userAgent);
    f.browser && (a.jPlayer.browser[f.browser] = !0, a.jPlayer.browser.version = f.version);
    f = a.jPlayer.uaPlatform(navigator.userAgent);
    f.platform && (a.jPlayer.platform[f.platform] = !0, a.jPlayer.platform.mobile = !f.tablet, a.jPlayer.platform.tablet = !!f.tablet);
    a.jPlayer.prototype = {count:0, version:{script:"2.2.0", needFlash:"2.2.0", flash:"unknown"}, options:{swfPath:"js", solution:"html, flash", supplied:"mp3", preload:"metadata", volume:0.8, muted:!1, wmode:"opaque", backgroundColor:"#000000", cssSelectorAncestor:"#jp_container_1", cssSelector:{videoPlay:".jp-video-play", play:".jp-play", pause:".jp-pause", stop:".jp-stop", seekBar:".jp-seek-bar", playBar:".jp-play-bar", mute:".jp-mute", unmute:".jp-unmute", volumeBar:".jp-volume-bar", volumeBarValue:".jp-volume-bar-value",
        volumeMax:".jp-volume-max", currentTime:".jp-current-time", duration:".jp-duration", fullScreen:".jp-full-screen", restoreScreen:".jp-restore-screen", repeat:".jp-repeat", repeatOff:".jp-repeat-off", gui:".jp-gui", noSolution:".jp-no-solution"}, fullScreen:!1, autohide:{restored:!1, full:!0, fadeIn:200, fadeOut:600, hold:1E3}, loop:!1, repeat:function(c) {
        c.jPlayer.options.loop ? a(this).unbind(".jPlayerRepeat").bind(a.jPlayer.event.ended + ".jPlayer.jPlayerRepeat", function() {
            a(this).jPlayer("play")
        }) : a(this).unbind(".jPlayerRepeat")
    }, nativeVideoControls:{}, noFullScreen:{msie:/msie [0-6]/, ipad:/ipad.*?os [0-4]/, iphone:/iphone/, ipod:/ipod/, android_pad:/android [0-3](?!.*?mobile)/, android_phone:/android.*?mobile/, blackberry:/blackberry/, windows_ce:/windows ce/, webos:/webos/}, noVolume:{ipad:/ipad/, iphone:/iphone/, ipod:/ipod/, android_pad:/android(?!.*?mobile)/, android_phone:/android.*?mobile/, blackberry:/blackberry/, windows_ce:/windows ce/, webos:/webos/, playbook:/playbook/}, verticalVolume:!1, idPrefix:"jp",
        noConflict:"jQuery", emulateHtml:!1, errorAlerts:!1, warningAlerts:!1}, optionsAudio:{size:{width:"0px", height:"0px", cssClass:""}, sizeFull:{width:"0px", height:"0px", cssClass:""}}, optionsVideo:{size:{width:"480px", height:"270px", cssClass:"jp-video-270p"}, sizeFull:{width:"100%", height:"100%", cssClass:"jp-video-full"}}, instances:{}, status:{src:"", media:{}, paused:!0, format:{}, formatType:"", waitForPlay:!0, waitForLoad:!0, srcSet:!1, video:!1, seekPercent:0, currentPercentRelative:0,
        currentPercentAbsolute:0, currentTime:0, duration:0, readyState:0, networkState:0, playbackRate:1, ended:0}, internal:{ready:!1}, solution:{html:!0, flash:!0}, format:{mp3:{codec:'audio/mpeg; codecs="mp3"', flashCanPlay:!0, media:"audio"}, m4a:{codec:'audio/mp4; codecs="mp4a.40.2"', flashCanPlay:!0, media:"audio"}, oga:{codec:'audio/ogg; codecs="vorbis"', flashCanPlay:!1, media:"audio"}, wav:{codec:'audio/wav; codecs="1"', flashCanPlay:!1, media:"audio"}, webma:{codec:'audio/webm; codecs="vorbis"',
        flashCanPlay:!1, media:"audio"}, fla:{codec:"audio/x-flv", flashCanPlay:!0, media:"audio"}, rtmpa:{codec:'audio/rtmp; codecs="rtmp"', flashCanPlay:!0, media:"audio"}, m4v:{codec:'video/mp4; codecs="avc1.42E01E, mp4a.40.2"', flashCanPlay:!0, media:"video"}, ogv:{codec:'video/ogg; codecs="theora, vorbis"', flashCanPlay:!1, media:"video"}, webmv:{codec:'video/webm; codecs="vorbis, vp8"', flashCanPlay:!1, media:"video"}, flv:{codec:"video/x-flv", flashCanPlay:!0, media:"video"}, rtmpv:{codec:'video/rtmp; codecs="rtmp"',
        flashCanPlay:!0, media:"video"}}, _init:function() {
        var c = this;
        this.element.empty();
        this.status = a.extend({}, this.status);
        this.internal = a.extend({}, this.internal);
        this.internal.domNode = this.element.get(0);
        this.formats = [];
        this.solutions = [];
        this.require = {};
        this.htmlElement = {};
        this.html = {};
        this.html.audio = {};
        this.html.video = {};
        this.flash = {};
        this.css = {};
        this.css.cs = {};
        this.css.jq = {};
        this.ancestorJq = [];
        this.options.volume = this._limitValue(this.options.volume, 0, 1);
        a.each(this.options.supplied.toLowerCase().split(","), function(b, e) {
            var d = e.replace(/^\s+|\s+$/g, "");
            if(c.format[d]) {
                var h = false;
                a.each(c.formats, function(b, c) {
                    if(d === c) {
                        h = true;
                        return false
                    }
                });
                h || c.formats.push(d)
            }
        });
        a.each(this.options.solution.toLowerCase().split(","), function(b, e) {
            var d = e.replace(/^\s+|\s+$/g, "");
            if(c.solution[d]) {
                var h = false;
                a.each(c.solutions, function(b, c) {
                    if(d === c) {
                        h = true;
                        return false
                    }
                });
                h || c.solutions.push(d)
            }
        });
        this.internal.instance = "jp_" + this.count;
        this.instances[this.internal.instance] = this.element;
        this.element.attr("id") || this.element.attr("id", this.options.idPrefix + "_jplayer_" + this.count);
        this.internal.self = a.extend({}, {id:this.element.attr("id"), jq:this.element});
        this.internal.audio = a.extend({}, {id:this.options.idPrefix + "_audio_" + this.count, jq:d});
        this.internal.video = a.extend({}, {id:this.options.idPrefix + "_video_" + this.count, jq:d});
        this.internal.flash = a.extend({}, {id:this.options.idPrefix + "_flash_" + this.count, jq:d, swf:this.options.swfPath + (this.options.swfPath.toLowerCase().slice(-4) !== ".swf" ? (this.options.swfPath && this.options.swfPath.slice(-1) !== "/" ? "/" : "") + "Jplayer.swf" : "")});
        this.internal.poster = a.extend({}, {id:this.options.idPrefix + "_poster_" + this.count, jq:d});
        a.each(a.jPlayer.event, function(b, a) {
            if(c.options[b] !== d) {
                c.element.bind(a + ".jPlayer", c.options[b]);
                c.options[b] = d
            }
        });
        this.require.audio = false;
        this.require.video = false;
        a.each(this.formats, function(b, a) {
            c.require[c.format[a].media] = true
        });
        this.options = this.require.video ? a.extend(true, {}, this.optionsVideo, this.options) : a.extend(true, {}, this.optionsAudio, this.options);
        this._setSize();
        this.status.nativeVideoControls = this._uaBlocklist(this.options.nativeVideoControls);
        this.status.noFullScreen = this._uaBlocklist(this.options.noFullScreen);
        this.status.noVolume = this._uaBlocklist(this.options.noVolume);
        this._restrictNativeVideoControls();
        this.htmlElement.poster = document.createElement("img");
        this.htmlElement.poster.id = this.internal.poster.id;
        this.htmlElement.poster.onload = function() {
            (!c.status.video || c.status.waitForPlay) && c.internal.poster.jq.show()
        };
        this.element.append(this.htmlElement.poster);
        this.internal.poster.jq = a("#" + this.internal.poster.id);
        this.internal.poster.jq.css({width:this.status.width, height:this.status.height});
        this.internal.poster.jq.hide();
        this.internal.poster.jq.bind("click.jPlayer", function() {
            c._trigger(a.jPlayer.event.click)
        });
        this.html.audio.available = false;
        if(this.require.audio) {
            this.htmlElement.audio = document.createElement("audio");
            this.htmlElement.audio.id = this.internal.audio.id;
            this.html.audio.available = !!this.htmlElement.audio.canPlayType && this._testCanPlayType(this.htmlElement.audio)
        }
        this.html.video.available = false;
        if(this.require.video) {
            this.htmlElement.video = document.createElement("video");
            this.htmlElement.video.id = this.internal.video.id;
            this.html.video.available = !!this.htmlElement.video.canPlayType && this._testCanPlayType(this.htmlElement.video)
        }
        this.flash.available = this._checkForFlash(10);
        this.html.canPlay = {};
        this.flash.canPlay = {};
        a.each(this.formats, function(b, a) {
            c.html.canPlay[a] = c.html[c.format[a].media].available && "" !== c.htmlElement[c.format[a].media].canPlayType(c.format[a].codec);
            c.flash.canPlay[a] = c.format[a].flashCanPlay && c.flash.available
        });
        this.html.desired = false;
        this.flash.desired = false;
        a.each(this.solutions, function(b, e) {
            if(b === 0) {
                c[e].desired = true
            }else {
                var d = false, h = false;
                a.each(c.formats, function(b, a) {
                    c[c.solutions[0]].canPlay[a] && (c.format[a].media === "video" ? h = true : d = true)
                });
                c[e].desired = c.require.audio && !d || c.require.video && !h
            }
        });
        this.html.support = {};
        this.flash.support = {};
        a.each(this.formats, function(b, a) {
            c.html.support[a] = c.html.canPlay[a] && c.html.desired;
            c.flash.support[a] = c.flash.canPlay[a] && c.flash.desired
        });
        this.html.used = false;
        this.flash.used = false;
        a.each(this.solutions, function(b, e) {
            a.each(c.formats, function(b, a) {
                if(c[e].support[a]) {
                    c[e].used = true;
                    return false
                }
            })
        });
        this._resetActive();
        this._resetGate();
        this._cssSelectorAncestor(this.options.cssSelectorAncestor);
        if(!this.html.used && !this.flash.used) {
            this._error({type:a.jPlayer.error.NO_SOLUTION, context:"{solution:'" + this.options.solution + "', supplied:'" + this.options.supplied + "'}", message:a.jPlayer.errorMsg.NO_SOLUTION, hint:a.jPlayer.errorHint.NO_SOLUTION});
            this.css.jq.noSolution.length && this.css.jq.noSolution.show()
        }else {
            this.css.jq.noSolution.length && this.css.jq.noSolution.hide()
        }
        if(this.flash.used) {
            var e, b = "jQuery=" + encodeURI(this.options.noConflict) + "&id=" + encodeURI(this.internal.self.id) + "&vol=" + this.options.volume + "&muted=" + this.options.muted;
            if(a.jPlayer.browser.msie && Number(a.jPlayer.browser.version) <= 8 && document.documentMode <= 8) {
                b = ['<param name="movie" value="' + this.internal.flash.swf + '" />', '<param name="FlashVars" value="' + b + '" />', '<param name="allowScriptAccess" value="always" />', '<param name="bgcolor" value="' + this.options.backgroundColor + '" />', '<param name="wmode" value="' + this.options.wmode + '" />'];
                e = document.createElement('<object id="' + this.internal.flash.id + '" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="0" height="0"></object>');
                for(var h = 0;h < b.length;h++) {
                    e.appendChild(document.createElement(b[h]))
                }
            }else {
                h = function(b, c, a) {
                    var e = document.createElement("param");
                    e.setAttribute("name", c);
                    e.setAttribute("value", a);
                    b.appendChild(e)
                };
                e = document.createElement("object");
                e.setAttribute("id", this.internal.flash.id);
                e.setAttribute("data", this.internal.flash.swf);
                e.setAttribute("type", "application/x-shockwave-flash");
                e.setAttribute("width", "1");
                e.setAttribute("height", "1");
                h(e, "flashvars", b);
                h(e, "allowscriptaccess", "always");
                h(e, "bgcolor", this.options.backgroundColor);
                h(e, "wmode", this.options.wmode)
            }
            this.element.append(e);
            this.internal.flash.jq = a(e)
        }
        if(this.html.used) {
            if(this.html.audio.available) {
                this._addHtmlEventListeners(this.htmlElement.audio, this.html.audio);
                this.element.append(this.htmlElement.audio);
                this.internal.audio.jq = a("#" + this.internal.audio.id)
            }
            if(this.html.video.available) {
                this._addHtmlEventListeners(this.htmlElement.video, this.html.video);
                this.element.append(this.htmlElement.video);
                this.internal.video.jq = a("#" + this.internal.video.id);
                this.status.nativeVideoControls ? this.internal.video.jq.css({width:this.status.width, height:this.status.height}) : this.internal.video.jq.css({width:"0px", height:"0px"});
                this.internal.video.jq.bind("click.jPlayer", function() {
                    c._trigger(a.jPlayer.event.click)
                })
            }
        }
        this.options.emulateHtml && this._emulateHtmlBridge();
        this.html.used && !this.flash.used && setTimeout(function() {
            c.internal.ready = true;
            c.version.flash = "n/a";
            c._trigger(a.jPlayer.event.repeat);
            c._trigger(a.jPlayer.event.ready)
        }, 100);
        this._updateNativeVideoControls();
        this._updateInterface();
        this._updateButtons(false);
        this._updateAutohide();
        this._updateVolume(this.options.volume);
        this._updateMute(this.options.muted);
        this.css.jq.videoPlay.length && this.css.jq.videoPlay.hide();
        a.jPlayer.prototype.count++
    }, destroy:function() {
        this.clearMedia();
        this._removeUiClass();
        this.css.jq.currentTime.length && this.css.jq.currentTime.text("");
        this.css.jq.duration.length && this.css.jq.duration.text("");
        a.each(this.css.jq, function(c, a) {
            a.length && a.unbind(".jPlayer")
        });
        this.internal.poster.jq.unbind(".jPlayer");
        this.internal.video.jq && this.internal.video.jq.unbind(".jPlayer");
        this.options.emulateHtml && this._destroyHtmlBridge();
        this.element.removeData("jPlayer");
        this.element.unbind(".jPlayer");
        this.element.empty();
        delete this.instances[this.internal.instance]
    }, enable:function() {
    }, disable:function() {
    }, _testCanPlayType:function(c) {
        try {
            c.canPlayType(this.format.mp3.codec);
            return true
        }catch(a) {
            return false
        }
    }, _uaBlocklist:function(c) {
        var e = navigator.userAgent.toLowerCase(), b = false;
        a.each(c, function(c, a) {
            if(a && a.test(e)) {
                b = true;
                return false
            }
        });
        return b
    }, _restrictNativeVideoControls:function() {
        if(this.require.audio && this.status.nativeVideoControls) {
            this.status.nativeVideoControls = false;
            this.status.noFullScreen = true
        }
    }, _updateNativeVideoControls:function() {
        if(this.html.video.available && this.html.used) {
            this.htmlElement.video.controls = this.status.nativeVideoControls;
            this._updateAutohide();
            if(this.status.nativeVideoControls && this.require.video) {
                this.internal.poster.jq.hide();
                this.internal.video.jq.css({width:this.status.width, height:this.status.height})
            }else {
                if(this.status.waitForPlay && this.status.video) {
                    this.internal.poster.jq.show();
                    this.internal.video.jq.css({width:"0px", height:"0px"})
                }
            }
        }
    }, _addHtmlEventListeners:function(c, e) {
        var b = this;
        c.preload = this.options.preload;
        c.muted = this.options.muted;
        c.volume = this.options.volume;
        c.addEventListener("progress", function() {
            if(e.gate) {
                b._getHtmlStatus(c);
                b._updateInterface();
                b._trigger(a.jPlayer.event.progress)
            }
        }, false);
        c.addEventListener("timeupdate", function() {
            if(e.gate) {
                b._getHtmlStatus(c);
                b._updateInterface();
                b._trigger(a.jPlayer.event.timeupdate)
            }
        }, false);
        c.addEventListener("durationchange", function() {
            if(e.gate) {
                b._getHtmlStatus(c);
                b._updateInterface();
                b._trigger(a.jPlayer.event.durationchange)
            }
        }, false);
        c.addEventListener("play", function() {
            if(e.gate) {
                b._updateButtons(true);
                b._html_checkWaitForPlay();
                b._trigger(a.jPlayer.event.play)
            }
        }, false);
        c.addEventListener("playing", function() {
            if(e.gate) {
                b._updateButtons(true);
                b._seeked();
                b._trigger(a.jPlayer.event.playing)
            }
        }, false);
        c.addEventListener("pause", function() {
            if(e.gate) {
                b._updateButtons(false);
                b._trigger(a.jPlayer.event.pause)
            }
        }, false);
        c.addEventListener("waiting", function() {
            if(e.gate) {
                b._seeking();
                b._trigger(a.jPlayer.event.waiting)
            }
        }, false);
        c.addEventListener("seeking", function() {
            if(e.gate) {
                b._seeking();
                b._trigger(a.jPlayer.event.seeking)
            }
        }, false);
        c.addEventListener("seeked", function() {
            if(e.gate) {
                b._seeked();
                b._trigger(a.jPlayer.event.seeked)
            }
        }, false);
        c.addEventListener("volumechange", function() {
            if(e.gate) {
                b.options.volume = c.volume;
                b.options.muted = c.muted;
                b._updateMute();
                b._updateVolume();
                b._trigger(a.jPlayer.event.volumechange)
            }
        }, false);
        c.addEventListener("suspend", function() {
            if(e.gate) {
                b._seeked();
                b._trigger(a.jPlayer.event.suspend)
            }
        }, false);
        c.addEventListener("ended", function() {
            if(e.gate) {
                if(!a.jPlayer.browser.webkit) {
                    b.htmlElement.media.currentTime = 0
                }
                b.htmlElement.media.pause();
                b._updateButtons(false);
                b._getHtmlStatus(c, true);
                b._updateInterface();
                b._trigger(a.jPlayer.event.ended)
            }
        }, false);
        c.addEventListener("error", function() {
            if(e.gate) {
                b._updateButtons(false);
                b._seeked();
                if(b.status.srcSet) {
                    clearTimeout(b.internal.htmlDlyCmdId);
                    b.status.waitForLoad = true;
                    b.status.waitForPlay = true;
                    b.status.video && !b.status.nativeVideoControls && b.internal.video.jq.css({width:"0px", height:"0px"});
                    b._validString(b.status.media.poster) && !b.status.nativeVideoControls && b.internal.poster.jq.show();
                    b.css.jq.videoPlay.length && b.css.jq.videoPlay.show();
                    b._error({type:a.jPlayer.error.URL, context:b.status.src, message:a.jPlayer.errorMsg.URL, hint:a.jPlayer.errorHint.URL})
                }
            }
        }, false);
        a.each(a.jPlayer.htmlEvent, function(d, g) {
            c.addEventListener(this, function() {
                e.gate && b._trigger(a.jPlayer.event[g])
            }, false)
        })
    }, _getHtmlStatus:function(c, a) {
        var b = 0, d = 0, g = 0, i = 0;
        if(isFinite(c.duration)) {
            this.status.duration = c.duration
        }
        b = c.currentTime;
        d = this.status.duration > 0 ? 100 * b / this.status.duration : 0;
        if(typeof c.seekable === "object" && c.seekable.length > 0) {
            g = this.status.duration > 0 ? 100 * c.seekable.end(c.seekable.length - 1) / this.status.duration : 100;
            i = this.status.duration > 0 ? 100 * c.currentTime / c.seekable.end(c.seekable.length - 1) : 0
        }else {
            g = 100;
            i = d
        }
        if(a) {
            d = i = b = 0
        }
        this.status.seekPercent = g;
        this.status.currentPercentRelative = i;
        this.status.currentPercentAbsolute = d;
        this.status.currentTime = b;
        this.status.readyState = c.readyState;
        this.status.networkState = c.networkState;
        this.status.playbackRate = c.playbackRate;
        this.status.ended = c.ended
    }, _resetStatus:function() {
        this.status = a.extend({}, this.status, a.jPlayer.prototype.status)
    }, _trigger:function(c, e, b) {
        c = a.Event(c);
        c.jPlayer = {};
        c.jPlayer.version = a.extend({}, this.version);
        c.jPlayer.options = a.extend(true, {}, this.options);
        c.jPlayer.status = a.extend(true, {}, this.status);
        c.jPlayer.html = a.extend(true, {}, this.html);
        c.jPlayer.flash = a.extend(true, {}, this.flash);
        if(e) {
            c.jPlayer.error = a.extend({}, e)
        }
        if(b) {
            c.jPlayer.warning = a.extend({}, b)
        }
        this.element.trigger(c)
    }, jPlayerFlashEvent:function(c, e) {
        if(c === a.jPlayer.event.ready) {
            if(this.internal.ready) {
                if(this.flash.gate) {
                    if(this.status.srcSet) {
                        var b = this.status.currentTime, d = this.status.paused;
                        this.setMedia(this.status.media);
                        b > 0 && (d ? this.pause(b) : this.play(b))
                    }
                    this._trigger(a.jPlayer.event.flashreset)
                }
            }else {
                this.internal.ready = true;
                this.internal.flash.jq.css({width:"0px", height:"0px"});
                this.version.flash = e.version;
                this.version.needFlash !== this.version.flash && this._error({type:a.jPlayer.error.VERSION, context:this.version.flash, message:a.jPlayer.errorMsg.VERSION + this.version.flash, hint:a.jPlayer.errorHint.VERSION});
                this._trigger(a.jPlayer.event.repeat);
                this._trigger(c)
            }
        }
        if(this.flash.gate) {
            switch(c) {
                case a.jPlayer.event.progress:
                    this._getFlashStatus(e);
                    this._updateInterface();
                    this._trigger(c);
                    break;
                case a.jPlayer.event.timeupdate:
                    this._getFlashStatus(e);
                    this._updateInterface();
                    this._trigger(c);
                    break;
                case a.jPlayer.event.play:
                    this._seeked();
                    this._updateButtons(true);
                    this._trigger(c);
                    break;
                case a.jPlayer.event.pause:
                    this._updateButtons(false);
                    this._trigger(c);
                    break;
                case a.jPlayer.event.ended:
                    this._updateButtons(false);
                    this._trigger(c);
                    break;
                case a.jPlayer.event.click:
                    this._trigger(c);
                    break;
                case a.jPlayer.event.error:
                    this.status.waitForLoad = true;
                    this.status.waitForPlay = true;
                    this.status.video && this.internal.flash.jq.css({width:"0px", height:"0px"});
                    this._validString(this.status.media.poster) && this.internal.poster.jq.show();
                    this.css.jq.videoPlay.length && this.status.video && this.css.jq.videoPlay.show();
                    this.status.video ? this._flash_setVideo(this.status.media) : this._flash_setAudio(this.status.media);
                    this._updateButtons(false);
                    this._error({type:a.jPlayer.error.URL, context:e.src, message:a.jPlayer.errorMsg.URL, hint:a.jPlayer.errorHint.URL});
                    break;
                case a.jPlayer.event.seeking:
                    this._seeking();
                    this._trigger(c);
                    break;
                case a.jPlayer.event.seeked:
                    this._seeked();
                    this._trigger(c);
                    break;
                case a.jPlayer.event.ready:
                    break;
                default:
                    this._trigger(c)
            }
        }
        return false
    }, _getFlashStatus:function(c) {
        this.status.seekPercent = c.seekPercent;
        this.status.currentPercentRelative = c.currentPercentRelative;
        this.status.currentPercentAbsolute = c.currentPercentAbsolute;
        this.status.currentTime = c.currentTime;
        this.status.duration = c.duration;
        this.status.readyState = 4;
        this.status.networkState = 0;
        this.status.playbackRate = 1;
        this.status.ended = false
    }, _updateButtons:function(c) {
        if(c !== d) {
            this.status.paused = !c;
            if(this.css.jq.play.length && this.css.jq.pause.length) {
                if(c) {
                    this.css.jq.play.hide();
                    this.css.jq.pause.show()
                }else {
                    this.css.jq.play.show();
                    this.css.jq.pause.hide()
                }
            }
        }
        if(this.css.jq.restoreScreen.length && this.css.jq.fullScreen.length) {
            if(this.status.noFullScreen) {
                this.css.jq.fullScreen.hide();
                this.css.jq.restoreScreen.hide()
            }else {
                if(this.options.fullScreen) {
                    this.css.jq.fullScreen.hide();
                    this.css.jq.restoreScreen.show()
                }else {
                    this.css.jq.fullScreen.show();
                    this.css.jq.restoreScreen.hide()
                }
            }
        }
        if(this.css.jq.repeat.length && this.css.jq.repeatOff.length) {
            if(this.options.loop) {
                this.css.jq.repeat.hide();
                this.css.jq.repeatOff.show()
            }else {
                this.css.jq.repeat.show();
                this.css.jq.repeatOff.hide()
            }
        }
    }, _updateInterface:function() {
        this.css.jq.seekBar.length && this.css.jq.seekBar.width(this.status.seekPercent + "%");
        this.css.jq.playBar.length && this.css.jq.playBar.width(this.status.currentPercentRelative + "%");
        this.css.jq.currentTime.length && this.css.jq.currentTime.text(a.jPlayer.convertTime(this.status.currentTime));
        this.css.jq.duration.length && this.css.jq.duration.text(a.jPlayer.convertTime(this.status.duration))
    }, _seeking:function() {
        this.css.jq.seekBar.length && this.css.jq.seekBar.addClass("jp-seeking-bg")
    }, _seeked:function() {
        this.css.jq.seekBar.length && this.css.jq.seekBar.removeClass("jp-seeking-bg")
    }, _resetGate:function() {
        this.html.audio.gate = false;
        this.html.video.gate = false;
        this.flash.gate = false
    }, _resetActive:function() {
        this.html.active = false;
        this.flash.active = false
    }, setMedia:function(c) {
        var e = this, b = false, d = this.status.media.poster !== c.poster;
        this._resetMedia();
        this._resetGate();
        this._resetActive();
        a.each(this.formats, function(d, h) {
            var f = e.format[h].media === "video";
            a.each(e.solutions, function(a, d) {
                if(e[d].support[h] && e._validString(c[h])) {
                    var g = d === "html";
                    if(f) {
                        if(g) {
                            e.html.video.gate = true;
                            e._html_setVideo(c);
                            e.html.active = true
                        }else {
                            e.flash.gate = true;
                            e._flash_setVideo(c);
                            e.flash.active = true
                        }
                        e.css.jq.videoPlay.length && e.css.jq.videoPlay.show();
                        e.status.video = true
                    }else {
                        if(g) {
                            e.html.audio.gate = true;
                            e._html_setAudio(c);
                            e.html.active = true
                        }else {
                            e.flash.gate = true;
                            e._flash_setAudio(c);
                            e.flash.active = true
                        }
                        e.css.jq.videoPlay.length && e.css.jq.videoPlay.hide();
                        e.status.video = false
                    }
                    b = true;
                    return false
                }
            });
            if(b) {
                return false
            }
        });
        if(b) {
            if((!this.status.nativeVideoControls || !this.html.video.gate) && this._validString(c.poster)) {
                d ? this.htmlElement.poster.src = c.poster : this.internal.poster.jq.show()
            }
            this.status.srcSet = true;
            this.status.media = a.extend({}, c);
            this._updateButtons(false);
            this._updateInterface()
        }else {
            this._error({type:a.jPlayer.error.NO_SUPPORT, context:"{supplied:'" + this.options.supplied + "'}", message:a.jPlayer.errorMsg.NO_SUPPORT, hint:a.jPlayer.errorHint.NO_SUPPORT})
        }
    }, _resetMedia:function() {
        this._resetStatus();
        this._updateButtons(false);
        this._updateInterface();
        this._seeked();
        this.internal.poster.jq.hide();
        clearTimeout(this.internal.htmlDlyCmdId);
        this.html.active ? this._html_resetMedia() : this.flash.active && this._flash_resetMedia()
    }, clearMedia:function() {
        this._resetMedia();
        this.html.active ? this._html_clearMedia() : this.flash.active && this._flash_clearMedia();
        this._resetGate();
        this._resetActive()
    }, load:function() {
        this.status.srcSet ? this.html.active ? this._html_load() : this.flash.active && this._flash_load() : this._urlNotSetError("load")
    }, play:function(c) {
        c = typeof c === "number" ? c : NaN;
        this.status.srcSet ? this.html.active ? this._html_play(c) : this.flash.active && this._flash_play(c) : this._urlNotSetError("play")
    }, videoPlay:function() {
        this.play()
    }, pause:function(c) {
        c = typeof c === "number" ? c : NaN;
        this.status.srcSet ? this.html.active ? this._html_pause(c) : this.flash.active && this._flash_pause(c) : this._urlNotSetError("pause")
    }, pauseOthers:function() {
        var c = this;
        a.each(this.instances, function(a, b) {
            c.element !== b && b.data("jPlayer").status.srcSet && b.jPlayer("pause")
        })
    }, stop:function() {
        this.status.srcSet ? this.html.active ? this._html_pause(0) : this.flash.active && this._flash_pause(0) : this._urlNotSetError("stop")
    }, playHead:function(c) {
        c = this._limitValue(c, 0, 100);
        this.status.srcSet ? this.html.active ? this._html_playHead(c) : this.flash.active && this._flash_playHead(c) : this._urlNotSetError("playHead")
    }, _muted:function(c) {
        this.options.muted = c;
        this.html.used && this._html_mute(c);
        this.flash.used && this._flash_mute(c);
        if(!this.html.video.gate && !this.html.audio.gate) {
            this._updateMute(c);
            this._updateVolume(this.options.volume);
            this._trigger(a.jPlayer.event.volumechange)
        }
    }, mute:function(c) {
        c = c === d ? true : !!c;
        this._muted(c)
    }, unmute:function(c) {
        c = c === d ? true : !!c;
        this._muted(!c)
    }, _updateMute:function(c) {
        if(c === d) {
            c = this.options.muted
        }
        if(this.css.jq.mute.length && this.css.jq.unmute.length) {
            if(this.status.noVolume) {
                this.css.jq.mute.hide();
                this.css.jq.unmute.hide()
            }else {
                if(c) {
                    this.css.jq.mute.hide();
                    this.css.jq.unmute.show()
                }else {
                    this.css.jq.mute.show();
                    this.css.jq.unmute.hide()
                }
            }
        }
    }, volume:function(c) {
        c = this._limitValue(c, 0, 1);
        this.options.volume = c;
        this.html.used && this._html_volume(c);
        this.flash.used && this._flash_volume(c);
        if(!this.html.video.gate && !this.html.audio.gate) {
            this._updateVolume(c);
            this._trigger(a.jPlayer.event.volumechange)
        }
    }, volumeBar:function(c) {
        if(this.css.jq.volumeBar.length) {
            var a = this.css.jq.volumeBar.offset(), b = c.pageX - a.left, d = this.css.jq.volumeBar.width(), c = this.css.jq.volumeBar.height() - c.pageY + a.top, a = this.css.jq.volumeBar.height();
            this.options.verticalVolume ? this.volume(c / a) : this.volume(b / d)
        }
        this.options.muted && this._muted(false)
    }, volumeBarValue:function(c) {
        this.volumeBar(c)
    }, _updateVolume:function(c) {
        if(c === d) {
            c = this.options.volume
        }
        c = this.options.muted ? 0 : c;
        if(this.status.noVolume) {
            this.css.jq.volumeBar.length && this.css.jq.volumeBar.hide();
            this.css.jq.volumeBarValue.length && this.css.jq.volumeBarValue.hide();
            this.css.jq.volumeMax.length && this.css.jq.volumeMax.hide()
        }else {
            this.css.jq.volumeBar.length && this.css.jq.volumeBar.show();
            if(this.css.jq.volumeBarValue.length) {
                this.css.jq.volumeBarValue.show();
                this.css.jq.volumeBarValue[this.options.verticalVolume ? "height" : "width"](c * 100 + "%")
            }
            this.css.jq.volumeMax.length && this.css.jq.volumeMax.show()
        }
    }, volumeMax:function() {
        this.volume(1);
        this.options.muted && this._muted(false)
    }, _cssSelectorAncestor:function(c) {
        var e = this;
        this.options.cssSelectorAncestor = c;
        this._removeUiClass();
        this.ancestorJq = c ? a(c) : [];
        c && this.ancestorJq.length !== 1 && this._warning({type:a.jPlayer.warning.CSS_SELECTOR_COUNT, context:c, message:a.jPlayer.warningMsg.CSS_SELECTOR_COUNT + this.ancestorJq.length + " found for cssSelectorAncestor.", hint:a.jPlayer.warningHint.CSS_SELECTOR_COUNT});
        this._addUiClass();
        a.each(this.options.cssSelector, function(b, c) {
            e._cssSelector(b, c)
        })
    }, _cssSelector:function(c, e) {
        var b = this;
        if(typeof e === "string") {
            if(a.jPlayer.prototype.options.cssSelector[c]) {
                this.css.jq[c] && this.css.jq[c].length && this.css.jq[c].unbind(".jPlayer");
                this.options.cssSelector[c] = e;
                this.css.cs[c] = this.options.cssSelectorAncestor + " " + e;
                this.css.jq[c] = e ? a(this.css.cs[c]) : [];
                this.css.jq[c].length && this.css.jq[c].bind("click.jPlayer", function(e) {
                    b[c](e);
                    a(this).blur();
                    return false
                });
                e && this.css.jq[c].length !== 1 && this._warning({type:a.jPlayer.warning.CSS_SELECTOR_COUNT, context:this.css.cs[c], message:a.jPlayer.warningMsg.CSS_SELECTOR_COUNT + this.css.jq[c].length + " found for " + c + " method.", hint:a.jPlayer.warningHint.CSS_SELECTOR_COUNT})
            }else {
                this._warning({type:a.jPlayer.warning.CSS_SELECTOR_METHOD, context:c, message:a.jPlayer.warningMsg.CSS_SELECTOR_METHOD, hint:a.jPlayer.warningHint.CSS_SELECTOR_METHOD})
            }
        }else {
            this._warning({type:a.jPlayer.warning.CSS_SELECTOR_STRING, context:e, message:a.jPlayer.warningMsg.CSS_SELECTOR_STRING, hint:a.jPlayer.warningHint.CSS_SELECTOR_STRING})
        }
    }, seekBar:function(c) {
        if(this.css.jq.seekBar) {
            var a = this.css.jq.seekBar.offset(), c = c.pageX - a.left, a = this.css.jq.seekBar.width();
            this.playHead(100 * c / a)
        }
    }, playBar:function(c) {
        this.seekBar(c)
    }, repeat:function() {
        this._loop(true)
    }, repeatOff:function() {
        this._loop(false)
    }, _loop:function(c) {
        if(this.options.loop !== c) {
            this.options.loop = c;
            this._updateButtons();
            this._trigger(a.jPlayer.event.repeat)
        }
    }, currentTime:function() {
    }, duration:function() {
    }, gui:function() {
    }, noSolution:function() {
    }, option:function(c, e) {
        var b = c;
        if(arguments.length === 0) {
            return a.extend(true, {}, this.options)
        }
        if(typeof c === "string") {
            var h = c.split(".");
            if(e === d) {
                for(var b = a.extend(true, {}, this.options), g = 0;g < h.length;g++) {
                    if(b[h[g]] !== d) {
                        b = b[h[g]]
                    }else {
                        this._warning({type:a.jPlayer.warning.OPTION_KEY, context:c, message:a.jPlayer.warningMsg.OPTION_KEY, hint:a.jPlayer.warningHint.OPTION_KEY});
                        return d
                    }
                }
                return b
            }
            for(var g = b = {}, i = 0;i < h.length;i++) {
                if(i < h.length - 1) {
                    g[h[i]] = {};
                    g = g[h[i]]
                }else {
                    g[h[i]] = e
                }
            }
        }
        this._setOptions(b);
        return this
    }, _setOptions:function(c) {
        var e = this;
        a.each(c, function(b, c) {
            e._setOption(b, c)
        });
        return this
    }, _setOption:function(c, e) {
        var b = this;
        switch(c) {
            case "volume":
                this.volume(e);
                break;
            case "muted":
                this._muted(e);
                break;
            case "cssSelectorAncestor":
                this._cssSelectorAncestor(e);
                break;
            case "cssSelector":
                a.each(e, function(c, a) {
                    b._cssSelector(c, a)
                });
                break;
            case "fullScreen":
                if(this.options[c] !== e) {
                    this._removeUiClass();
                    this.options[c] = e;
                    this._refreshSize()
                }
                break;
            case "size":
                !this.options.fullScreen && this.options[c].cssClass !== e.cssClass && this._removeUiClass();
                this.options[c] = a.extend({}, this.options[c], e);
                this._refreshSize();
                break;
            case "sizeFull":
                this.options.fullScreen && this.options[c].cssClass !== e.cssClass && this._removeUiClass();
                this.options[c] = a.extend({}, this.options[c], e);
                this._refreshSize();
                break;
            case "autohide":
                this.options[c] = a.extend({}, this.options[c], e);
                this._updateAutohide();
                break;
            case "loop":
                this._loop(e);
                break;
            case "nativeVideoControls":
                this.options[c] = a.extend({}, this.options[c], e);
                this.status.nativeVideoControls = this._uaBlocklist(this.options.nativeVideoControls);
                this._restrictNativeVideoControls();
                this._updateNativeVideoControls();
                break;
            case "noFullScreen":
                this.options[c] = a.extend({}, this.options[c], e);
                this.status.nativeVideoControls = this._uaBlocklist(this.options.nativeVideoControls);
                this.status.noFullScreen = this._uaBlocklist(this.options.noFullScreen);
                this._restrictNativeVideoControls();
                this._updateButtons();
                break;
            case "noVolume":
                this.options[c] = a.extend({}, this.options[c], e);
                this.status.noVolume = this._uaBlocklist(this.options.noVolume);
                this._updateVolume();
                this._updateMute();
                break;
            case "emulateHtml":
                if(this.options[c] !== e) {
                    (this.options[c] = e) ? this._emulateHtmlBridge() : this._destroyHtmlBridge()
                }
        }
        return this
    }, _refreshSize:function() {
        this._setSize();
        this._addUiClass();
        this._updateSize();
        this._updateButtons();
        this._updateAutohide();
        this._trigger(a.jPlayer.event.resize)
    }, _setSize:function() {
        if(this.options.fullScreen) {
            this.status.width = this.options.sizeFull.width;
            this.status.height = this.options.sizeFull.height;
            this.status.cssClass = this.options.sizeFull.cssClass
        }else {
            this.status.width = this.options.size.width;
            this.status.height = this.options.size.height;
            this.status.cssClass = this.options.size.cssClass
        }
        this.element.css({width:this.status.width, height:this.status.height})
    }, _addUiClass:function() {
        this.ancestorJq.length && this.ancestorJq.addClass(this.status.cssClass)
    }, _removeUiClass:function() {
        this.ancestorJq.length && this.ancestorJq.removeClass(this.status.cssClass)
    }, _updateSize:function() {
        this.internal.poster.jq.css({width:this.status.width, height:this.status.height});
        !this.status.waitForPlay && this.html.active && this.status.video || this.html.video.available && this.html.used && this.status.nativeVideoControls ? this.internal.video.jq.css({width:this.status.width, height:this.status.height}) : !this.status.waitForPlay && (this.flash.active && this.status.video) && this.internal.flash.jq.css({width:this.status.width, height:this.status.height})
    }, _updateAutohide:function() {
        var c = this, a = function() {
            c.css.jq.gui.fadeIn(c.options.autohide.fadeIn, function() {
                clearTimeout(c.internal.autohideId);
                c.internal.autohideId = setTimeout(function() {
                    c.css.jq.gui.fadeOut(c.options.autohide.fadeOut)
                }, c.options.autohide.hold)
            })
        };
        if(this.css.jq.gui.length) {
            this.css.jq.gui.stop(true, true);
            clearTimeout(this.internal.autohideId);
            this.element.unbind(".jPlayerAutohide");
            this.css.jq.gui.unbind(".jPlayerAutohide");
            if(this.status.nativeVideoControls) {
                this.css.jq.gui.hide()
            }else {
                if(this.options.fullScreen && this.options.autohide.full || !this.options.fullScreen && this.options.autohide.restored) {
                    this.element.bind("mousemove.jPlayer.jPlayerAutohide", a);
                    this.css.jq.gui.bind("mousemove.jPlayer.jPlayerAutohide", a);
                    this.css.jq.gui.hide()
                }else {
                    this.css.jq.gui.show()
                }
            }
        }
    }, fullScreen:function() {
        this._setOption("fullScreen", true)
    }, restoreScreen:function() {
        this._setOption("fullScreen", false)
    }, _html_initMedia:function() {
        this.htmlElement.media.src = this.status.src;
        this.options.preload !== "none" && this._html_load();
        this._trigger(a.jPlayer.event.timeupdate)
    }, _html_setAudio:function(c) {
        var e = this;
        a.each(this.formats, function(b, a) {
            if(e.html.support[a] && c[a]) {
                e.status.src = c[a];
                e.status.format[a] = true;
                e.status.formatType = a;
                return false
            }
        });
        this.htmlElement.media = this.htmlElement.audio;
        this._html_initMedia()
    }, _html_setVideo:function(c) {
        var e = this;
        a.each(this.formats, function(b, a) {
            if(e.html.support[a] && c[a]) {
                e.status.src = c[a];
                e.status.format[a] = true;
                e.status.formatType = a;
                return false
            }
        });
        if(this.status.nativeVideoControls) {
            this.htmlElement.video.poster = this._validString(c.poster) ? c.poster : ""
        }
        this.htmlElement.media = this.htmlElement.video;
        this._html_initMedia()
    }, _html_resetMedia:function() {
        if(this.htmlElement.media) {
            this.htmlElement.media.id === this.internal.video.id && !this.status.nativeVideoControls && this.internal.video.jq.css({width:"0px", height:"0px"});
            this.htmlElement.media.pause()
        }
    }, _html_clearMedia:function() {
        if(this.htmlElement.media) {
            this.htmlElement.media.src = "";
            this.htmlElement.media.load()
        }
    }, _html_load:function() {
        if(this.status.waitForLoad) {
            this.status.waitForLoad = false;
            this.htmlElement.media.load()
        }
        clearTimeout(this.internal.htmlDlyCmdId)
    }, _html_play:function(c) {
        var a = this;
        this._html_load();
        this.htmlElement.media.play();
        if(!isNaN(c)) {
            try {
                this.htmlElement.media.currentTime = c
            }catch(b) {
                this.internal.htmlDlyCmdId = setTimeout(function() {
                    a.play(c)
                }, 100);
                return
            }
        }
        this._html_checkWaitForPlay()
    }, _html_pause:function(c) {
        var a = this;
        c > 0 ? this._html_load() : clearTimeout(this.internal.htmlDlyCmdId);
        this.htmlElement.media.pause();
        if(!isNaN(c)) {
            try {
                this.htmlElement.media.currentTime = c
            }catch(b) {
                this.internal.htmlDlyCmdId = setTimeout(function() {
                    a.pause(c)
                }, 100);
                return
            }
        }
        c > 0 && this._html_checkWaitForPlay()
    }, _html_playHead:function(c) {
        var a = this;
        this._html_load();
        try {
            if(typeof this.htmlElement.media.seekable === "object" && this.htmlElement.media.seekable.length > 0) {
                this.htmlElement.media.currentTime = c * this.htmlElement.media.seekable.end(this.htmlElement.media.seekable.length - 1) / 100
            }else {
                if(this.htmlElement.media.duration > 0 && !isNaN(this.htmlElement.media.duration)) {
                    this.htmlElement.media.currentTime = c * this.htmlElement.media.duration / 100
                }else {
                    throw"e";
                }
            }
        }catch(b) {
            this.internal.htmlDlyCmdId = setTimeout(function() {
                a.playHead(c)
            }, 100);
            return
        }
        this.status.waitForLoad || this._html_checkWaitForPlay()
    }, _html_checkWaitForPlay:function() {
        if(this.status.waitForPlay) {
            this.status.waitForPlay = false;
            this.css.jq.videoPlay.length && this.css.jq.videoPlay.hide();
            if(this.status.video) {
                this.internal.poster.jq.hide();
                this.internal.video.jq.css({width:this.status.width, height:this.status.height})
            }
        }
    }, _html_volume:function(c) {
        if(this.html.audio.available) {
            this.htmlElement.audio.volume = c
        }
        if(this.html.video.available) {
            this.htmlElement.video.volume = c
        }
    }, _html_mute:function(c) {
        if(this.html.audio.available) {
            this.htmlElement.audio.muted = c
        }
        if(this.html.video.available) {
            this.htmlElement.video.muted = c
        }
    }, _flash_setAudio:function(c) {
        var e = this;
        try {
            a.each(this.formats, function(b, a) {
                if(e.flash.support[a] && c[a]) {
                    switch(a) {
                        case "m4a":
                            ;
                        case "fla":
                            e._getMovie().fl_setAudio_m4a(c[a]);
                            break;
                        case "mp3":
                            e._getMovie().fl_setAudio_mp3(c[a]);
                            break;
                        case "rtmpa":
                            e._getMovie().fl_setAudio_rtmp(c[a])
                    }
                    e.status.src = c[a];
                    e.status.format[a] = true;
                    e.status.formatType = a;
                    return false
                }
            });
            if(this.options.preload === "auto") {
                this._flash_load();
                this.status.waitForLoad = false
            }
        }catch(b) {
            this._flashError(b)
        }
    }, _flash_setVideo:function(c) {
        var e = this;
        try {
            a.each(this.formats, function(b, a) {
                if(e.flash.support[a] && c[a]) {
                    switch(a) {
                        case "m4v":
                            ;
                        case "flv":
                            e._getMovie().fl_setVideo_m4v(c[a]);
                            break;
                        case "rtmpv":
                            e._getMovie().fl_setVideo_rtmp(c[a])
                    }
                    e.status.src = c[a];
                    e.status.format[a] = true;
                    e.status.formatType = a;
                    return false
                }
            });
            if(this.options.preload === "auto") {
                this._flash_load();
                this.status.waitForLoad = false
            }
        }catch(b) {
            this._flashError(b)
        }
    }, _flash_resetMedia:function() {
        this.internal.flash.jq.css({width:"0px", height:"0px"});
        this._flash_pause(NaN)
    }, _flash_clearMedia:function() {
        try {
            this._getMovie().fl_clearMedia()
        }catch(a) {
            this._flashError(a)
        }
    }, _flash_load:function() {
        try {
            this._getMovie().fl_load()
        }catch(a) {
            this._flashError(a)
        }
        this.status.waitForLoad = false
    }, _flash_play:function(a) {
        try {
            this._getMovie().fl_play(a)
        }catch(e) {
            this._flashError(e)
        }
        this.status.waitForLoad = false;
        this._flash_checkWaitForPlay()
    }, _flash_pause:function(a) {
        try {
            this._getMovie().fl_pause(a)
        }catch(e) {
            this._flashError(e)
        }
        if(a > 0) {
            this.status.waitForLoad = false;
            this._flash_checkWaitForPlay()
        }
    }, _flash_playHead:function(a) {
        try {
            this._getMovie().fl_play_head(a)
        }catch(e) {
            this._flashError(e)
        }
        this.status.waitForLoad || this._flash_checkWaitForPlay()
    }, _flash_checkWaitForPlay:function() {
        if(this.status.waitForPlay) {
            this.status.waitForPlay = false;
            this.css.jq.videoPlay.length && this.css.jq.videoPlay.hide();
            if(this.status.video) {
                this.internal.poster.jq.hide();
                this.internal.flash.jq.css({width:this.status.width, height:this.status.height})
            }
        }
    }, _flash_volume:function(a) {
        try {
            this._getMovie().fl_volume(a)
        }catch(e) {
            this._flashError(e)
        }
    }, _flash_mute:function(a) {
        try {
            this._getMovie().fl_mute(a)
        }catch(e) {
            this._flashError(e)
        }
    }, _getMovie:function() {
        return document[this.internal.flash.id]
    }, _checkForFlash:function(a) {
        var e = false, b;
        if(window.ActiveXObject) {
            try {
                new ActiveXObject("ShockwaveFlash.ShockwaveFlash." + a);
                e = true
            }catch(d) {
            }
        }else {
            if(navigator.plugins && navigator.mimeTypes.length > 0) {
                (b = navigator.plugins["Shockwave Flash"]) && navigator.plugins["Shockwave Flash"].description.replace(/.*\s(\d+\.\d+).*/, "$1") >= a && (e = true)
            }
        }
        return e
    }, _validString:function(a) {
        return a && typeof a === "string"
    }, _limitValue:function(a, e, b) {
        return a < e ? e : a > b ? b : a
    }, _urlNotSetError:function(c) {
        this._error({type:a.jPlayer.error.URL_NOT_SET, context:c, message:a.jPlayer.errorMsg.URL_NOT_SET, hint:a.jPlayer.errorHint.URL_NOT_SET})
    }, _flashError:function(c) {
        var e;
        e = this.internal.ready ? "FLASH_DISABLED" : "FLASH";
        this._error({type:a.jPlayer.error[e], context:this.internal.flash.swf, message:a.jPlayer.errorMsg[e] + c.message, hint:a.jPlayer.errorHint[e]});
        this.internal.flash.jq.css({width:"1px", height:"1px"})
    }, _error:function(c) {
        this._trigger(a.jPlayer.event.error, c);
        this.options.errorAlerts && this._alert("Error!" + (c.message ? "\n\n" + c.message : "") + (c.hint ? "\n\n" + c.hint : "") + "\n\nContext: " + c.context)
    }, _warning:function(c) {
        this._trigger(a.jPlayer.event.warning, d, c);
        this.options.warningAlerts && this._alert("Warning!" + (c.message ? "\n\n" + c.message : "") + (c.hint ? "\n\n" + c.hint : "") + "\n\nContext: " + c.context)
    }, _alert:function(a) {
        alert("jPlayer " + this.version.script + " : id='" + this.internal.self.id + "' : " + a)
    }, _emulateHtmlBridge:function() {
        var c = this;
        a.each(a.jPlayer.emulateMethods.split(/\s+/g), function(a, b) {
            c.internal.domNode[b] = function(a) {
                c[b](a)
            }
        });
        a.each(a.jPlayer.event, function(e, b) {
            var d = true;
            a.each(a.jPlayer.reservedEvent.split(/\s+/g), function(b, a) {
                if(a === e) {
                    return d = false
                }
            });
            d && c.element.bind(b + ".jPlayer.jPlayerHtml", function() {
                c._emulateHtmlUpdate();
                var b = document.createEvent("Event");
                b.initEvent(e, false, true);
                c.internal.domNode.dispatchEvent(b)
            })
        })
    }, _emulateHtmlUpdate:function() {
        var c = this;
        a.each(a.jPlayer.emulateStatus.split(/\s+/g), function(a, b) {
            c.internal.domNode[b] = c.status[b]
        });
        a.each(a.jPlayer.emulateOptions.split(/\s+/g), function(a, b) {
            c.internal.domNode[b] = c.options[b]
        })
    }, _destroyHtmlBridge:function() {
        var c = this;
        this.element.unbind(".jPlayerHtml");
        a.each((a.jPlayer.emulateMethods + " " + a.jPlayer.emulateStatus + " " + a.jPlayer.emulateOptions).split(/\s+/g), function(a, b) {
            delete c.internal.domNode[b]
        })
    }};
    a.jPlayer.error = {FLASH:"e_flash", FLASH_DISABLED:"e_flash_disabled", NO_SOLUTION:"e_no_solution", NO_SUPPORT:"e_no_support", URL:"e_url", URL_NOT_SET:"e_url_not_set", VERSION:"e_version"};
    a.jPlayer.errorMsg = {FLASH:"jPlayer's Flash fallback is not configured correctly, or a command was issued before the jPlayer Ready event. Details: ", FLASH_DISABLED:"jPlayer's Flash fallback has been disabled by the browser due to the CSS rules you have used. Details: ", NO_SOLUTION:"No solution can be found by jPlayer in this browser. Neither HTML nor Flash can be used.", NO_SUPPORT:"It is not possible to play any media format provided in setMedia() on this browser using your current options.",
        URL:"Media URL could not be loaded.", URL_NOT_SET:"Attempt to issue media playback commands, while no media url is set.", VERSION:"jPlayer " + a.jPlayer.prototype.version.script + " needs Jplayer.swf version " + a.jPlayer.prototype.version.needFlash + " but found "};
    a.jPlayer.errorHint = {FLASH:"Check your swfPath option and that Jplayer.swf is there.", FLASH_DISABLED:"Check that you have not display:none; the jPlayer entity or any ancestor.", NO_SOLUTION:"Review the jPlayer options: support and supplied.", NO_SUPPORT:"Video or audio formats defined in the supplied option are missing.", URL:"Check media URL is valid.", URL_NOT_SET:"Use setMedia() to set the media URL.", VERSION:"Update jPlayer files."};
    a.jPlayer.warning = {CSS_SELECTOR_COUNT:"e_css_selector_count", CSS_SELECTOR_METHOD:"e_css_selector_method", CSS_SELECTOR_STRING:"e_css_selector_string", OPTION_KEY:"e_option_key"};
    a.jPlayer.warningMsg = {CSS_SELECTOR_COUNT:"The number of css selectors found did not equal one: ", CSS_SELECTOR_METHOD:"The methodName given in jPlayer('cssSelector') is not a valid jPlayer method.", CSS_SELECTOR_STRING:"The methodCssSelector given in jPlayer('cssSelector') is not a String or is empty.", OPTION_KEY:"The option requested in jPlayer('option') is undefined."};
    a.jPlayer.warningHint = {CSS_SELECTOR_COUNT:"Check your css selector and the ancestor.", CSS_SELECTOR_METHOD:"Check your method name.", CSS_SELECTOR_STRING:"Check your css selector is a string.", OPTION_KEY:"Check your option name."}
})(jQuery);
(function(a) {
    function d(c) {
        var b = c || window.event, d = [].slice.call(arguments, 1), g = 0, i = 0, f = 0, c = a.event.fix(b);
        c.type = "mousewheel";
        b.wheelDelta && (g = b.wheelDelta / 120);
        b.detail && (g = -b.detail / 3);
        f = g;
        void 0 !== b.axis && b.axis === b.HORIZONTAL_AXIS && (f = 0, i = -1 * g);
        void 0 !== b.wheelDeltaY && (f = b.wheelDeltaY / 120);
        void 0 !== b.wheelDeltaX && (i = -1 * b.wheelDeltaX / 120);
        d.unshift(c, g, i, f);
        return(a.event.dispatch || a.event.handle).apply(this, d)
    }
    var f = ["DOMMouseScroll", "mousewheel"];
    if(a.event.fixHooks) {
        for(var c = f.length;c;) {
            a.event.fixHooks[f[--c]] = a.event.mouseHooks
        }
    }
    a.event.special.mousewheel = {setup:function() {
        if(this.addEventListener) {
            for(var a = f.length;a;) {
                this.addEventListener(f[--a], d, !1)
            }
        }else {
            this.onmousewheel = d
        }
    }, teardown:function() {
        if(this.removeEventListener) {
            for(var a = f.length;a;) {
                this.removeEventListener(f[--a], d, !1)
            }
        }else {
            this.onmousewheel = null
        }
    }};
    a.fn.extend({mousewheel:function(a) {
        return a ? this.bind("mousewheel", a) : this.trigger("mousewheel")
    }, unmousewheel:function(a) {
        return this.unbind("mousewheel", a)
    }})
})(jQuery);
(function(a, d) {
    var f, c, e, b;
    function h(b) {
        if(b.pageX) {
            return[b.pageX, b.pageY]
        }
        var a = d, c = b.target.ownerDocument, e = c.body, c = c.documentElement;
        return[b.clientX + (a.pageXOffset || c.scrollLeft || e.scrollLeft || 0) - (c.clientLeft || e.clientLeft || 0), b.clientY + (a.pageYOffset || c.scrollTop || e.scrollTop || 0) - (c.clientTop || e.clientTop || 0)]
    }
    b = void 0;
    f = 0;
    c = 1;
    e = 2;
    var g = {disable:!1, cancel:"input", cursor:"move", distance:5, helper:"original", getPos:function(b) {
        var a = b.offset(), c = a.top;
        return[a.left + b.attr("offsetWidth") / 2, c + b.attr("offsetHeight") / 2]
    }}, i = "__DrAg_DrOp__", j = function(b, c) {
        this._moElement$ = b;
        this._moMover$ = null;
        this._moContainer$ = c && c.container && a(c.container);
        this._moOptions = a.extend({}, g, c);
        this._mnState = e;
        this._init()
    };
    j.prototype = {option:function(b, a) {
        var c = this._moOptions;
        return a ? (c[b] = a, this) : c[b]
    }, _init:function() {
        function c(h) {
            var g = [];
            b && (g = b[f]);
            for(var l = 0;l < g.length;l++) {
                var j = g[l];
                j != e._moElement$.size() && a.trigger(j, i, [{state:e._mnState, cursorPos:h, pos:d.getPos(e._moMover$)}])
            }
        }
        var e = this, d = e._moOptions;
        (d.handle ? e._moElement$.find(d.handle) : e._moElement$).bind("mousedown", function(b) {
            b.preventDefault();
            if(!(d.disable || d.lockx && d.locky)) {
                var a = e._moElement$.offset();
                e._moOrgPos = {_nMouseX:b.clientX, _nMouseY:b.clientY, _nDomX:a.left - (parseInt(e._moElement$.css("margin-left")) || 0), _nDomY:a.top - (parseInt(e._moElement$.css("margin-top")) || 0)};
                e._move()
            }
        });
        var g = null, f = d.group;
        f && e._moElement$.bind("dragStart", function(b) {
            c(h(b));
            a(b.target.ownerDocument.body).css("cursor", d.cursor)
        }).bind("drag", function(b) {
                clearTimeout(g);
                var a = h(b);
                g = setTimeout(function() {
                    c(a)
                })
            }).bind("dragStop", function(b) {
                c(h(b));
                a(b.target.ownerDocument.body).css("cursor", "")
            })
    }, _move:function() {
        function b(k) {
            i.setCapture ? (i.setCapture(!0), a(i).bind("losecapture", d)) : (j.captureEvents(Event.MOUSEMOVE | Event.MOUSEUP), a.bind(j).bind("blur", d));
            k.preventDefault();
            j.getSelection ? j.getSelection().removeAllRanges() : l.selection.empty();
            var m = h._moOrgPos, C = m._nMouseY, m = Math.abs(m._nMouseX - k.clientX), C = Math.abs(C - k.clientY);
            if(h._mnState == e) {
                if(m > g.distance || C > g.distance) {
                    h._mnState = f, h._start(k), h._moElement$.trigger("dragStart", [k, {helper:h._moMover$, position:{left:0, right:0}, offset:{left:0, right:0}}])
                }
            }else {
                h._mnState = c, h._drag(k), h._moElement$.trigger("drag", [k, {helper:h._moMover$, position:{left:0, right:0}, offset:{left:0, right:0}}])
            }
        }
        function d(c) {
            h._mnState != e && (h._mnState = e, h._moElement$.trigger("dragStop", [c, {helper:h._moMover$, position:{left:0, right:0}, offset:{left:0, right:0}}]), h._stop(c));
            a(l).unbind("mousemove", b).unbind("mouseup", d);
            i.releaseCapture ? (i.releaseCapture(), a(i).unbind("losecapture", d)) : (j.releaseEvents(Event.MOUSEMOVE | Event.MOUSEUP), a(j).unbind("blur", d))
        }
        var h = this, g = h._moOptions, i = h._moElement$[0], l = i.ownerDocument, j = l.parentWindow || l.defaultView;
        a(l).bind("mousemove", b);
        a(l).bind("mouseup", d)
    }, _start:function(b) {
        var a = this._moOptions;
        this._moMover$ = this._getMover(b);
        this._moMover = this._moMover$[0];
        this._moOrgStyle = {_zIndex:this._moMover$.css("zIndex"), _opacity:this._moMover$.css("opacity")};
        this._moMover$.css("zIndex", "10001").css("opacity", a.opacity);
        this._moMover$.css("display", "block")
    }, _drag:function(b) {
        var a = this._moOptions;
        with(this._moMover.style) {
            if(a.cursorAt) {
                b = h(b), left = b[0] + (a.cursorAt.left || 0) + "px", top = b[1] + (a.cursorAt.right || 0) + "px"
            }else {
                for(var c = this._moMover$.parent("*").offset() || {left:0, top:0}, e = this._moMover, d = {top:0, left:0}, g = e.offsetParent;e && e != g;) {
                    d.top += e.scrollTop, d.left += e.scrollLeft, e = e.parentNode
                }
                e = this._moOrgPos;
                a.lockx || (left = e._nDomX + b.clientX - e._nMouseX - c.left + d.left + "px");
                a.locky || (top = e._nDomY + b.clientY - e._nMouseY - c.top + d.top + "px");
                if(this._moContainer$) {
                    var b = this._moMover$.offset(), c = this._moContainer$.offset(), d = this._moMover.clientHeight, e = this._moMover.clientWidth, g = this._moContainer$.innerHeight(), i = this._moContainer$.innerWidth(), f = Math.ceil(this._moContainer$.css("border-left-width").replace(/px/, "")), l = Math.ceil(this._moContainer$.css("border-top-width").replace(/px/, ""));
                    b.left < c.left + f && !a.lockx ? left = this._moMover.offsetLeft + (c.left + f - b.left) + "px" : b.left + e > c.left + f + i && !a.lockx && (left = this._moMover.offsetLeft + (c.left + f + i) - (b.left + e) + "px");
                    b.top < c.top + l && !a.locky ? top = this._moMover.offsetTop + (c.top + l - b.top) + "px" : b.top + d > c.top + l + g && !a.locky && (top = this._moMover.offsetTop + (c.top + l + g) - (b.top + d) + "px")
                }
            }
        }
    }, _stop:function() {
        var b = this._moOptions.helper;
        "original" === b ? this._moMover$.css("zIndex", this._moOrgStyle._zIndex).css("opacity", this._moOrgStyle._opacity) : "clone" === b ? (this._moElement$.css("opacity", 1), this._moMover$.remove(), this._moMover = null) : this._moMover$.css("left", "-1000px").css("top", "-1000px").hide()
    }, _getMover:function(b) {
        var c = this._moElement$, e = this._moOptions, d = e.helper, h;
        h = "original" === d ? c : "clone" === d ? a(c[0].cloneNode(!0)) : a(d);
        var g = e.cursorAt ? b.clientY + (e.cursorAt.right || 0) + "px" : c.attr("offsetTop") - (parseInt(c.css("margin-top")) || 0) + "px", b = e.cursorAt ? b.clientX + (e.cursorAt.left || 0) + "px" : c.attr("offsetLeft") - (parseInt(c.css("margin-left")) || 0) + "px";
        h.css("top", g).css("left", b).css("position", "absolute");
        "clone" === d && c.parent("*").append(h);
        return h
    }};
    var l = {getPos:function(b) {
        var a = b.offset(), c = b.attr("offsetWidth"), b = b.attr("offsetHeight");
        return[a.top, a.left + c, a.top + b, a.left]
    }}, k = function(b, c) {
        this._moElement$ = b;
        this._moOptions = a.extend({}, l, c);
        this._mnState = void 0;
        this._init()
    };
    k.prototype = {option:function(b, a) {
        var c = this._moOptions;
        a && (c[b] = a);
        return c[b]
    }, _init:function() {
        var b = this;
        b._moOptions.group && b._moElement$.bind(i, function(a) {
            b.listen(a)
        })
    }, listen:function(b) {
        var a = this, c = b.state, d = b.pos, h = b.cursorPos, g = a._mnState;
        a._mnState = a._isOver(a._moOptions.overByCursor ? h : d, a._moOptions.getPos(a._moElement$)) ? c == e ? 2 : 0 : 1;
        g != a._mnState && 2 != g && (0 == a._mnState ? a._mnDropOverTimer = setTimeout(function() {
            a._moElement$.trigger("dropOverLong", [b])
        }, 800) : 1 == a._mnState && clearTimeout(a._mnDropOverTimer), a._moElement$.trigger(["dropOver", "dropOut", "drop"][a._mnState], [b]))
    }, _isOver:function(b, a) {
        var c = b[0], e = b[1], d = a[1], h = a[0], g = a[2];
        return c > a[3] && c < d && e > h && e < g
    }};
    a.fn.draggable = function(b) {
        this.each(function() {
            new j(a(this), b)
        });
        return this
    };
    a.fn.droppable = function(c) {
        var e, d = c.group || "default-group";
        b = b || {};
        e = b[d] || [];
        this.each(function(b) {
            var d = !1;
            new k(a(this), c);
            for(var h = 0;h < e.length;h++) {
                b == e[h] && (d = !0)
            }
            !d && e.push(b)
        });
        b[d] = e;
        return this
    }
})(jQuery, this);
window.jQuery && function(a) {
    a.extend({xml2json:function(d, f) {
        function c(d, h) {
            if(!d) {
                return null
            }
            var g = "", k = null;
            e(d.localName || d.nodeName);
            d.childNodes && 0 < d.childNodes.length && a.each(d.childNodes, function(a, d) {
                var h = d.nodeType, i = e(d.localName || d.nodeName), f = d.text || d.nodeValue || "";
                8 != h && (3 == h || 4 == h || !i ? f.match(/^\s+$/) || (g += f.replace(/^\s+/, "").replace(/\s+$/, "")) : (k = k || {}, k[i] ? (k[i].length || (k[i] = b(k[i])), k[i] = b(k[i]), k[i][k[i].length] = c(d, !0), k[i].length = k[i].length) : k[i] = c(d)))
            });
            d.attributes && 0 < d.attributes.length && (k = k || {}, a.each(d.attributes, function(a, c) {
                var d = e(c.name), h = c.value;
                k[d] ? (k[cnn] = b(k[cnn]), k[d][k[d].length] = h, k[d].length = k[d].length) : k[d] = h
            }));
            if(k) {
                k = a.extend("" != g ? new String(g) : {}, k || {});
                if(g = k.text ? ("object" == typeof k.text ? k.text : [k.text || ""]).concat([g]) : g) {
                    k.text = g
                }
                g = ""
            }
            var m = k || g;
            if(f) {
                g && (m = {});
                if(g = m.text || g || "") {
                    m.text = g
                }
                h || (m = b(m))
            }
            return m
        }
        if(!d) {
            return{}
        }
        var e = function(b) {
            return("" + (b || "")).replace(/-/g, "_")
        }, b = function(b) {
            a.isArray(b) || (b = [b]);
            b.length = b.length;
            return b
        };
        "string" == typeof d && (d = a.text2xml(d));
        if(d.nodeType) {
            if(3 == d.nodeType || 4 == d.nodeType) {
                return d.nodeValue
            }
            var h = 9 == d.nodeType ? d.documentElement : d, g = c(h, !0), h = d = null;
            return g
        }
    }, text2xml:function(d) {
        var f;
        try {
            var c = a.browser.msie ? new ActiveXObject("Microsoft.XMLDOM") : new DOMParser;
            c.async = !1
        }catch(e) {
            throw Error("XML Parser could not be instantiated");
        }
        try {
            f = a.browser.msie ? c.loadXML(d) ? c : !1 : c.parseFromString(d, "text/xml")
        }catch(b) {
            throw Error("Error parsing XML string");
        }
        return f
    }})
}(jQuery);
(function(a, d) {
    var f = function(c, b) {
        function h() {
            i.outerHeight(!0) == g._nContentHeight && f.innerHeight() == g._nContainerHeight || g._resize()
        }
        var g = this;
        g._option = {opacity:0.8, rate:5, deltaRate:10, minHeight:20, maxMouseWheelContentScroll:50};
        a.extend(g._option, b);
        var i = g._oContent$ = c, f = g._oContainer$ = c.parent(), l = g._oBarBox$ = a("<div/>").addClass("scrollbarBox"), k = g._oBar$ = a("<div/>").addClass("scrollbar");
        k.offsetTop = 0;
        k.setTop = function(b) {
            k.offsetTop = b;
            return k
        };
        k.getTop = function() {
            return k.offsetTop
        };
        k.setHeight = function(b) {
            b = Math.floor(b);
            k.css("height", b);
            g._nBarScrollHeight = g._nContainerHeight - b;
            return k
        };
        k.moveTo = function(b, a) {
            k.isShow() && (0 > b && (b = 0), b > g._nBarScrollHeight && (b = g._nBarScrollHeight), k.setTop(b).css("top", Math.round(b)), a || k.moved())
        };
        k.moved = function() {
            k.appear();
            var b = Math.ceil(g._getScrollDestPos());
            i.css("top", b);
            g._option.onscroll && g._option.onscroll(b);
            return k
        };
        k.timeout = null;
        k.opacity = g._option.opacity;
        k.autoDisappear = !0;
        k.appear = function() {
            k.timeout && (clearTimeout(k.timeout), k.timeout = null);
            k.stop(!0).css({opacity:k.opacity});
            k.autoDisappear && k.disappear()
        };
        k.disappear = function() {
            k.timeout || (k.timeout = setTimeout(function() {
                k.stop(!0).animate({opacity:0}, "fast")
            }, 1E3))
        };
        g._resize();
        k.css({position:"absolute", right:"0", top:"0", display:"none"}).draggable({container:f, lockx:!0, distance:0}).on("drag", function() {
            k.setTop(k.position().top).moved()
        });
        l.css({position:"absolute", right:"0", top:"0", height:"100%"}).on("mouseenter", function() {
            k.autoDisappear = !1;
            k.appear()
        }).on("mouseleave", function() {
                k.autoDisappear = !0;
                k.disappear()
            });
        i.css({position:"absolute"});
        f.append(l.append(k)).css({"overflow-y":"hidden", position:"relative"}).mousewheel(function(b, a) {
            var c = parseInt(k.css("top")) - a * g._nDeltaRate;
            k.moveTo(c)
        }).on("mouseenter", function() {
                k.appear()
            }).data({scrollTop:function(b) {
                if(!b && 0 != b) {
                    return-parseInt(i.css("top"))
                }
                k.moveTo(parseInt(b) / g._nRate);
                return null
            }, heightChanged:function() {
                h()
            }, scrollBarDestroy:function() {
                g.destroy()
            }});
        g._oContentHeightInterval = setInterval(h, 500);
        debug(function() {
            d.scrollBars || (d.scrollBars = {});
            var b = 0, a;
            for(a in d.scrollBars) {
                ++b
            }
            b = f.attr("id") || f.attr("class") || i.attr("id") || i.attr("class") || "noname" + b;
            d.scrollBars[b] = g
        });
        return{resize:function() {
            g._resize()
        }, moveTo:function(b) {
            k.moveTo(b)
        }, destroy:function() {
            g.destroy()
        }}
    };
    f.prototype = {constructor:f, _resize:function() {
        this._nContentHeight = this._oContent$.outerHeight(!0);
        this._nContainerHeight = this._oContainer$.innerHeight();
        this._nRate = this._option.rate;
        this._nDeltaRate = this._option.deltaRate;
        this._nContentScrollBottom = this._nContentHeight - this._nContainerHeight;
        if(this._nContentHeight <= this._nContainerHeight) {
            this._oContent$.css("top", "0"), this._oBar$.hide()
        }else {
            var a = this._getBarHeightWithRate(), b = -parseInt(this._oContent$.css("top")) / this._nRate;
            this._reCalculateDeltaRate();
            this._oBar$.setHeight(a).moveTo(b);
            this._oBar$.show().appear()
        }
    }, _getBarHeightWithRate:function() {
        var a = this._option.minHeight, b = a, b = this._nContainerHeight - this._nContentScrollBottom / this._nRate;
        b < a && (b = a, this._nRate = this._nContentScrollBottom / (this._nContainerHeight - b));
        return b
    }, _getScrollDestPos:function() {
        var a = this._oBar$.getTop() * this._nRate, a = a <= this._nContentScrollBottom ? a : this._nContentScrollBottom;
        return-a
    }, _reCalculateDeltaRate:function() {
        var a = this._option.maxMouseWheelContentScroll;
        this._nDeltaRate * this._nRate <= a || (this._nDeltaRate = Math.floor(a / this._nRate), 1 > this._nDeltaRate && (this._nDeltaRate = 1))
    }, destroy:function() {
        this._oBarBox$.remove();
        this._oContainer$.removeData("scrollTop heightChanged scrollBarDestroy").off("mouseenter").unmousewheel();
        clearInterval(this._oContentHeightInterval);
        delete this
    }};
    a.fn.scrollable = function(c) {
        var b = this, d;
        b.each(function() {
            b.scrollBar = d = new f(a(this), c)
        });
        return d
    };
    var c = a.fn.scrollTop;
    a.fn.scrollTop = function(a) {
        if(!this.data("scrollTop")) {
            return c.apply(this, arguments)
        }
        this.data("heightChanged") && this.data("heightChanged")();
        var b = this.data("scrollTop")(a);
        return!b && 0 != b ? this : b
    }
})(jQuery, this);
(function(a, d) {
    function f(b) {
        var b = a(b), c = b.offset();
        return[c.top, c.left + b.width(), c.top + b.height(), c.left, b.width(), b.height()]
    }
    var c = function(b, a, c) {
        this._moResizeDom = null;
        this._moOptions = {maxContainer:null, minWidth:0, minHeight:0, scale:0};
        this._moCallBacks = {onready:function() {
        }, onresize:function() {
        }, oncomplete:function() {
        }};
        this._init(b, a, c)
    };
    c.prototype = {setTriggers:function(b) {
        var c = this;
        a.each(b, function(b, d) {
            a(d).off("mousedown").on("mousedown", function(b) {
                c._start(b, c._getResizeFunc(d[1]))
            })
        });
        a(c._moResizeDom).mousewheel(function(b, a) {
            var d = 6 * a;
            c._computeOriPos(b);
            c._getResizeFunc("left-top")(-d, -d);
            c._computeOriPos(b);
            c._getResizeFunc("right-bottom")(d, d);
            c._moCallBacks.onresize.call(c);
            b.preventDefault()
        })
    }, getResizeDom:function() {
        return this._moResizeDom
    }, _init:function(b, c, d) {
        this._moResizeDom = b;
        this._moDocument = b.ownerDocument;
        this._moWindow = this._moDocument.parentWindow || this._moDocument.defaultView;
        a.extend(this._moOptions, c);
        a.extend(this._moCallBacks, d)
    }, _start:function(b, c) {
        var d = this;
        d._computeOriPos(b);
        d._moCallBacks.onready.call(d);
        b.stopPropagation();
        a(d._moDocument).off("mousemove").on("mousemove", d._moOnMouseMove = function(b) {
            d._resize(b, c)
        });
        a(d._moDocument).off("mouseup").on("mouseup", d._moOnMouseUp = function(b) {
            d._stop(b, c)
        });
        d._moResizeDom.setCapture && (d._moResizeDom.setCapture(), a(d._moResizeDom).off("losecapture").on("losecapture", d._moOnMouseUp));
        return d
    }, _resize:function(b, c) {
        this._moWindow.getSelection ? this._moWindow.getSelection().removeAllRanges() : this._moDocument.selection.empty();
        var d = b.clientX + a(document.body).scrollLeft(), e = b.clientY + a(document.body).scrollTop();
        c.call(this, d - this._mnMouseX, e - this._mnMouseY);
        this._moCallBacks.onresize.call(this);
        return this
    }, _stop:function() {
        a(this._moDocument).off("mousemove", this._moOnMouseMove).off("mouseup", this._moOnMouseUp);
        this._moResizeDom.releaseCapture && (this._moResizeDom.releaseCapture(), a(this._moResizeDom).off("losecapture", this._moOnMouseUp));
        this._moCallBacks.oncomplete.call(this);
        return this
    }, _computeOriPos:function(b) {
        var c = this._moResizeDom, d = this._moOptions.maxContainer;
        this._mnMouseX = b.clientX + a(document.body).scrollLeft();
        this._mnMouseY = b.clientY + a(document.body).scrollTop();
        this._moPos = f(c);
        this._mnTop = c.offsetTop;
        this._mnLeft = c.offsetLeft;
        this._mnHeight = a.browser.msie ? this._moPos[5] : c.clientHeight;
        this._mnWidth = a.browser.msie ? this._moPos[4] : c.clientWidth;
        d && (this._moContainerPos = d && f(d), this._mnDiffTop = this._moContainerPos[0] - this._moPos[0], this._mnDiffLeft = this._moContainerPos[3] - this._moPos[3], this._mnDiffBottom = this._moContainerPos[2] - this._moPos[2], this._mnDiffRight = this._moContainerPos[1] - this._moPos[1]);
        return this
    }, _computeDiff:function(b, a, c, d, e, f, k, m) {
        var n = this._moOptions;
        n.scale ? c && !d ? a = b / n.scale * (f && k || e && m ? -1 : 1) : !c && d ? b = a * n.scale * (f && k || e && m ? -1 : 1) : c && d && (Math.abs(b) > Math.abs(n.scale * a) ? a = b / n.scale * (f && k || e && m ? -1 : 1) : Math.abs(b) < Math.abs(n.scale * a) && (b = a * n.scale * (f && k || e && m ? -1 : 1))) : (b = c ? b : 0, a = d ? a : 0);
        if(n.maxContainer) {
            var q = f && this._moPos[3] + b < this._moContainerPos[3], p = k && this._moPos[2] + a > this._moContainerPos[2], s = m && this._moPos[1] + b > this._moContainerPos[1];
            if(e && this._moPos[0] + a < this._moContainerPos[0]) {
                return this._computeDiff(n.scale ? 0 : b, this._mnDiffTop, c, !0, e, f, k, m)
            }
            if(q) {
                return this._computeDiff(this._mnDiffLeft, n.scale ? 0 : a, !0, d, e, f, k, m)
            }
            if(p) {
                return this._computeDiff(n.scale ? 0 : b, this._mnDiffBottom, c, !0, e, f, k, m)
            }
            if(s) {
                return this._computeDiff(this._mnDiffRight, n.scale ? 0 : a, !0, d, e, f, k, m)
            }
        }
        c = this._mnHeight + (k ? a : -a) < n.minHeight;
        return this._mnWidth + (m ? b : -b) < n.minWidth || c ? null : [b, a]
    }, _getResizeFunc:function(b) {
        function a(b, c) {
            k.top = f._mnTop + c + "px";
            k.height = f._mnHeight - c + "px"
        }
        function c(b) {
            k.left = f._mnLeft + b + "px";
            k.width = f._mnWidth - b + "px"
        }
        function d(b, a) {
            k.height = f._mnHeight + a + "px"
        }
        function e(b) {
            k.width = f._mnWidth + b + "px"
        }
        var f = this, k = f._moResizeDom.style;
        switch(b.toLowerCase()) {
            case "top":
                return function(b, d) {
                    var e = f._computeDiff(b, d, !1, !0, !0, !0);
                    e && a(e[0], e[1]);
                    e && c(e[0], e[1])
                };
            case "left":
                return function(b, d) {
                    var e = f._computeDiff(b, d, !0, !1, !0, !0);
                    e && a(e[0], e[1]);
                    e && c(e[0], e[1])
                };
            case "bottom":
                return function(b, a) {
                    var c = f._computeDiff(b, a, !1, !0, !1, !1, !0, !0);
                    c && d(c[0], c[1]);
                    c && e(c[0], c[1])
                };
            case "right":
                return function(b, a) {
                    var c = f._computeDiff(b, a, !0, !1, !1, !1, !0, !0);
                    c && d(c[0], c[1]);
                    c && e(c[0], c[1])
                };
            case "left-top":
                return function(b, d) {
                    var e = f._computeDiff(b, d, !0, !0, !0, !0);
                    e && a(e[0], e[1]);
                    e && c(e[0], e[1])
                };
            case "right-top":
                return function(b, c) {
                    var d = f._computeDiff(b, c, !0, !0, !0, !1, !1, !0);
                    d && a(d[0], d[1]);
                    d && e(d[0], d[1])
                };
            case "left-bottom":
                return function(b, a) {
                    var e = f._computeDiff(b, a, !0, !0, !1, !0, !0, !1);
                    e && d(e[0], e[1]);
                    e && c(e[0], e[1])
                };
            case "right-bottom":
                return function(b, a) {
                    var c = f._computeDiff(b, a, !0, !0, !1, !1, !0, !0);
                    c && d(c[0], c[1]);
                    c && e(c[0], c[1])
                };
            default:
                return function() {
                    debug("undifined direction")
                }
        }
    }};
    var e = d.QMImgCropper = function(b, a, c) {
        this._moContainer = null;
        this._msImgPath = "";
        this._moPreviewImgs = [];
        this._moOptions = {resizeScale:1, previewDoms:[]};
        this._moCallBacks = {onready:function() {
        }, onmove:function() {
        }, onresize:function() {
        }};
        this._init(b, a, c)
    };
    e.prototype = {setImg:function(b) {
        this._msImgPath = b;
        this._setLayer()
    }, getImg:function() {
        return this._msImgPath
    }, getPos:function() {
        var b = this._getCropperPos();
        return[Math.round(b[0] * this._mnImageHeight / this._mnImgStyleHeight), Math.round(b[3] * this._mnImageWidth / this._mnImgStyleWidth), Math.round(b[4] * this._mnImageHeight / this._mnImgStyleHeight), Math.round(b[5] * this._mnImageWidth / this._mnImgStyleWidth), Math.round(this._mnImageWidth), Math.round(this._mnImageHeight)]
    }, _init:function(b, c, d) {
        this._moContainer = b;
        this._moDocument = b.ownerDocument;
        this._moWindow = this._moDocument.parentWindow || this._moDocument.defaultView;
        a.extend(this._moOptions, c);
        a.extend(this._moCallBacks, d)
    }, _setLayer:function() {
        function b() {
            var e = d.clientHeight, f = d.clientWidth;
            a(c._moWrapper).show();
            c._mnImageHeight = c._moBaseImg.height;
            c._mnImageWidth = c._moBaseImg.width;
            var i = c._getSize([e, f], [c._mnImageHeight, c._mnImageWidth]);
            c._mnImgStyleHeight = i[0];
            c._mnImgStyleWidth = i[1];
            with(c._moWrapper.style) {
                height = i[0] + "px", width = i[1] + "px", top = (e - i[0]) / 2 + "px", left = (f - i[1]) / 2 + "px"
            }
            with(c._moBaseImg.style) {
                height = i[0] + "px", width = i[1] + "px", position = "absolute"
            }
            a(c._moBaseImg).css("opacity", 0.6);
            with(c._moCropperImg.style) {
                height = c._mnImgStyleHeight + "px", width = c._mnImgStyleWidth + "px", position = "absolute", zIndex = "100"
            }
            c._moPreviewImgs = [];
            e = 0;
            for(f = c._moOptions.previewDoms;e < f.length;e++) {
                i = c._moDocument.createElement("img"), i.src = c._msImgPath, i.style.position = "absolute", f[e].style.overflow = "hidden", f[e].style.position = "relative", f[e].innerHTML = "", c._moPreviewImgs.push(f[e].appendChild(i))
            }
            c._setCropper();
            a(c._moBaseImg).off("load", b);
            c._moCallBacks.onready()
        }
        var c = this, d = c._moContainer, e = c._moDocument.createElement("div"), f = c._moDocument.createElement("img"), l = c._moDocument.createElement("img");
        d.innerHTML = "";
        e.style.position = "relative";
        e.style.backgroundColor = "#000";
        e.style.display = "none";
        c._moWrapper = d.appendChild(e);
        c._moBaseImg = c._moWrapper.appendChild(f);
        c._moCropperImg = c._moWrapper.appendChild(l);
        a(c._moBaseImg).on("load", b);
        f.src = l.src = c._msImgPath;
        return c
    }, _setCropper:function() {
        function b() {
            var b = d._getCropperPos();
            d._moCropperImg.style.clip = "rect(" + (b[0] + 1) + "px," + (b[1] + 1) + "px," + (b[2] + 1) + "px," + (b[3] + 1) + "px)";
            d._setPreview()
        }
        var d = this, f = a.now(), i = d._moOptions.resizeScale, j, l, k, m;
        j = 0;
        a.browser.msie || (j = 2);
        d._mnImgStyleWidth / d._mnImgStyleHeight > i ? (k = d._mnImgStyleHeight - j, m = k * i, j = 0, l = (d._mnImgStyleWidth - m) / 2) : (m = d._mnImgStyleWidth - j, k = m / i, j = (d._mnImgStyleHeight - k) / 2, l = 0);
        a(d._moWrapper).append(a.tmpl(e.TMPL.cropper, {_id:f, top:j + "px", left:l + "px", height:k + "px", width:m + "px"}));
        d._moCropper = a("#resizedom_" + f, d._moDocument)[0];
        var n = [[a("#rUp_" + f, d._moDocument)[0], "top"], [a("#rLeft_" + f, d._moDocument)[0], "left"], [a("#rDown_" + f, d._moDocument)[0], "bottom"], [a("#rRight_" + f, d._moDocument)[0], "right"], [a("#rLeftUp_" + f, d._moDocument)[0], "left-top"], [a("#rLeftDown_" + f, d._moDocument)[0], "left-bottom"], [a("#rRightUp_" + f, d._moDocument)[0], "right-top"], [a("#rRightDown_" + f, d._moDocument)[0], "right-bottom"]];
        (new c(d._moCropper, {maxContainer:d._moWrapper, scale:i}, {onresize:function() {
            b();
            d._moCallBacks.onresize()
        }})).setTriggers(n);
        a(d._moCropper).draggable({container:d._moWrapper}).bind("dragStart", function() {
            a.each(n, function(b, c) {
                a(c[0]).hide()
            })
        }).bind("drag", function() {
                b();
                d._moCallBacks.onmove()
            }).bind("dragStop", function() {
                a.each(n, function(b, c) {
                    a(c[0]).show()
                })
            });
        b();
        return d
    }, _setPreview:function() {
        for(var b = this._moOptions.previewDoms, a = this._moPreviewImgs, c = this._getCropperPos(), d = 0;d < a.length;d++) {
            var e = b[d].clientHeight, f = b[d].clientWidth;
            with(a[d].style) {
                c[4] && c[5] && (height = this._mnImgStyleHeight * e / c[4] + "px", width = this._mnImgStyleWidth * f / c[5] + "px", top = -(c[0] * e / c[4]) + "px", left = -(c[3] * f / c[5]) + "px")
            }
        }
        return this
    }, _getSize:function(b, c) {
        if(b[0] > c[0] && b[1] > c[1]) {
            return c
        }
        if(c[0] * b[1] > c[1] * b[1]) {
            var a = b[0] * c[1] / (c[0] || 1);
            return a > b[1] ? [b[1] * b[0] / a, b[1]] : [b[0], a]
        }
        a = c[0] * b[1] / (c[1] || 1);
        return a > b[0] ? [b[0], b[1] * b[0] / a] : [a, b[1]]
    }, _getCropperPos:function() {
        var b = this._moCropper;
        return[b.offsetTop, b.offsetLeft + b.clientWidth, b.offsetTop + b.clientHeight, b.offsetLeft, b.clientHeight, b.clientWidth]
    }};
    e.TMPL = {cropper:'<div id="resizedom_<#=_id#>" style="border:1px dashed #ccc; width:<#=width#>; height:<#=height#>; top:<#=top#>; left:<#=left#>; position:absolute;cursor:move;z-index:200;"><div id="rRightDown_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:nw-resize;right:-4px;bottom:-4px;background-color:#00F;"> </div><div id="rLeftDown_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:ne-resize;left:-4px;bottom:-4px;"> </div><div id="rRightUp_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:ne-resize;right:-4px;top:-4px;"> </div><div id="rLeftUp_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:nw-resize;left:-4px;top:-4px;"> </div><div id="rRight_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:e-resize;right:-4px;top:50%;margin-top:-4px;"> </div><div id="rLeft_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:e-resize;left:-4px;top:50%;margin-top:-4px;"> </div><div id="rUp_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:n-resize;top:-4px;left:50%;margin-left:-4px;"> </div><div id="rDown_<#=_id#>" style="position:absolute;background:#FFF;border: 1px solid #333;width: 6px;height: 6px;z-index:500;font-size:0;opacity: 0.5;filter:alpha(opacity=50);cursor:n-resize;bottom:-4px;left:50%;margin-left:-4px;"> </div><div style="filter: alpha(opacity:0); opacity:0;BACKGROUND-COLOR: #fff; width: 100%; height: 100%; font-size: 0px;"/></div>'}
})(jQuery, this);
(function(a) {
    function d(c, a) {
        var b = a || window;
        return(b = b[c] || b.document[c]) && (b.length ? b[b.length - 1] : b)
    }
    function f(c) {
        if(!(this._mId = c.id)) {
            throw Error(0, "config.id can't use null");
        }
        if(!(this._mWin = c.win)) {
            throw Error(0, "config.win win is null");
        }
        this._mFlash = c.flash;
        this._moConstructor = this.constructor;
        this._mEvent = c;
        this._initlize()
    }
    _goStatic = f;
    _goClass = _goStatic.prototype;
    _goStatic.get = function(c, a) {
        var b = a[this._CONST._CACHES];
        return b && b[c]
    };
    _goStatic.getFlashVer = function() {
        var c = "", a = -1, b = -1, d = -1, f = navigator.plugins;
        if(f && f.length) {
            for(var i = 0, j = f.length;i < j;i++) {
                var l = f[i];
                if(-1 != l.name.indexOf("Shockwave Flash")) {
                    c = l.description.split("Shockwave Flash ")[1];
                    a = parseFloat(c);
                    d = parseInt(c.split("r")[1]);
                    b = parseInt(c.split("b")[1]);
                    break
                }
            }
        }else {
            try {
                if(i = new ActiveXObject("ShockwaveFlash.ShockwaveFlash")) {
                    c = i.GetVariable("$version").split(" ")[1], j = c.split(","), a = parseFloat(j.join(".")), d = parseInt(j[2]), b = parseInt(j[3])
                }
            }catch(k) {
            }
        }
        return{version:(isNaN(a) ? -1 : a) || -1, build:(isNaN(d) ? -1 : d) || -1, beta:(isNaN(b) ? -1 : b) || -1, desc:c}
    };
    _goStatic.isSupported = function() {
        var a = this.getFlashVer();
        return 10 <= a.version || 9 == a.version && 50 < a.build
    };
    _goStatic._CONST = {_TIMEOUT:5E3, _CACHES:"qmFlashCaches_ASDr431gGas", _CALLBACK:"onFlashEvent_ASDr431gGas"};
    _goClass.getFlash = function() {
        return this._mFlash || d(this._mId, this._mWin)
    };
    _goClass.isDisabled = function() {
        return this._mDisabled || !1
    };
    _goClass.disable = function(a) {
        this._mDisabled = !1 != a;
        return this
    };
    _goClass.setup = function(a) {
        function d(e, f) {
            try {
                a.call(b, e, f)
            }catch(i) {
            }
        }
        var b = this;
        this._getLoadedPercent(function(a) {
            100 == a ? setTimeout(function() {
                try {
                    if(!b.getFlash().setup(f._CONST._CALLBACK, b._mId)) {
                        return d(!1, "setuperr")
                    }
                }catch(a) {
                    return d(!1, "nosetup")
                }
                d(!0)
            }) : "number" != typeof a && d(!1, a)
        })
    };
    _goClass._getLoadedPercent = function(c) {
        function d(a) {
            try {
                c.call(b, a)
            }catch(e) {
            }
        }
        var b = this, h = this.getFlash();
        if(!h) {
            return d("notfound")
        }
        var g = 0;
        (function() {
            var b = arguments.callee;
            b._startTime || (b._startTime = a.now());
            var c = 0, l = !1;
            try {
                c = h.PercentLoaded()
            }catch(k) {
                l = !0
            }
            c != g && d(g = c);
            100 != c && (a.now() - b._startTime > f._CONST._TIMEOUT ? d(l ? "noflash" : "timeout") : setTimeout(b, 100))
        })()
    };
    _goClass._initlize = function() {
        var a = this._mWin, d = this._moConstructor._CONST, b = d._CACHES, d = d._CALLBACK;
        a[b] || (a[b] = new a.Object);
        a[b][this._mId] = this;
        a[d] || (a[d] = function() {
            var d = arguments[1], e = a[b][arguments[0]];
            if(e && "function" == typeof e._mEvent[d]) {
                for(var f = [], j = 2, l = arguments.length;j < l;j++) {
                    f.push(arguments[j])
                }
                e._mEvent[d].apply(e, f)
            }
        })
    };
    a.generateFlashCode = function(c, d, b, f) {
        var g = [], i = [], j = [], f = f || {}, l = a.browser.msie ? '<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" <#=codebase#> <#=attr#> <#=id#> ><#=param#></object>' : '<embed <#=embed#> type="application/x-shockwave-flash" <#=pluginspage#>  <#=name#> <#=id#> ></embed>';
        f.allowscriptaccess = b && b.allowscriptaccess || "always";
        f.quality = "high";
        for(var k in f) {
            var m = {name:k, value:f[k]};
            i.push(a.tmpl('<param name="<#=name#>" value="<#=value#>" />', m));
            j.push(a.tmpl(" <#=name#>=<#=value#> ", m))
        }
        for(k in b) {
            m = {name:k, value:b[k]}, g.push(a.tmpl(" <#=name#>=<#=value#> ", m)), j.push(a.tmpl(" <#=name#>=<#=value#> ", m))
        }
        d && (i.push(a.tmpl('<param name="<#=name#>" value="<#=value#>" />', {name:"movie", value:d})), j.push(a.tmpl(" <#=name#>=<#=value#> ", {name:"src", value:d})));
        return a.tmpl(l, {id:c && [' id="', c, '"'].join(""), name:c && [' name="', c, '"'].join(""), attr:g.join(""), param:i.join(""), embed:j.join(""), codebase:"https:" == location.protocol ? "" : 'codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" ', pluginspage:"https:" == location.protocol ? "" : 'pluginspage="http://www.adobe.com/cn/products/flashplayer" '})
    };
    a.getFlash = d;
    a.qmFlash = f
})(jQuery, this);
(function(a, d) {
    var f = {};
    d.WebMM = a.extend(d.WebMM || {}, {triggerEvent:function(c, e, b) {
        setTimeout(function() {
            a(d.document.body).trigger("globalevent", {type:c, range:!b && "all", data:e});
            f[c] && f[c](e)
        }, 0)
    }, addEventListener:function(a, d) {
        f[a] = d
    }})
})(jQuery, this);
(function(a, d) {
    var f = {};
    d.model = d.model || function(c, d) {
        if(!d) {
            return f[c]
        }
        f[c] = a.extend(f[c] || {}, d)
    }
})(jQuery, WebMM, this);
(function(a, d) {
    var f = {};
    d.logic = d.logic || function(c, d) {
        if(!d) {
            return f[c]
        }
        f[c] = a.extend(f[c] || {}, d)
    }
})(jQuery, WebMM, this);
(function(a, d, f, c) {
    function e(b, c) {
        var d = a.parseURLParam(b);
        d.ctrl = b.split("?")[0];
        c && (d.child = arguments.callee(c));
        return d
    }
    function b(b) {
        b = a("#" + b);
        return b.length && b
    }
    var h = {base:Class({init:function(b, a) {
        var c = a || {};
        this._moChildren = {};
        this._msName = b;
        this._moDom$ = c.oDom$.attr("ctrl", 1);
        this._moDom$[0].ctrl = this;
        this._moParent = c.oParent;
        c.oParent = this;
        this._moComponets = d.ctrlComponents(this, c)
    }, getName:function() {
        return this._msName
    }, getParent:function() {
        return this._moParent
    }, _changeActive:function(b, a) {
        if(this._msLastHash != a) {
            this._moParams = b;
            this._msLastHash = a;
            for(var c = 0, d = this._moComponets.length;c < d;c++) {
                this._moComponets[c].active(b)
            }
            this.active(b)
        }
    }, active:function() {
    }, _inactive:function() {
        this._msLastHash = "";
        this.inactive && this.inactive()
    }, isActive:function() {
        return!!this._mbActive
    }, back:function() {
        a.history.back()
    }, isTopView:function() {
        return this.isActive() && !this._msActiveChild
    }, dispatch:function(b, a, c) {
        b = "on" + b.toLowerCase();
        this[b] && this[b](a, c)
    }, getDom$:function() {
        return this._moDom$
    }, getParam:function(b) {
        return(this._moParams || {})[b]
    }, html:function(b) {
        return b == c ? this._moDom$.html() : this._moDom$.html(b)
    }, onglobalevent:function(b) {
        var a = b.type;
        if("all" == b.range) {
            for(var c in this._moChildren) {
                this._moChildren[c].onglobalevent(b)
            }
        }else {
            if(this._msActiveChild) {
                this._moChildren[this._msActiveChild].onglobalevent(b)
            }
        }
        this[a] && this[a](b.data);
        c = 0;
        for(var d = this._moComponets.length;c < d;c++) {
            this._moComponets[c][a] && this._moComponets[c][a](b.data)
        }
    }, onhashchange:function(c, f) {
        var h = c.replace(/^#/ig, "").split("/"), g = e(h[0], h[1]);
        this._changeActive(g, h[0]);
        g.child && g.child.ctrl ? (g = g.child.ctrl, this._moChildren[g] || (this._moChildren[g] = d.ctrl(g, {oDom$:b(g, this._moDom$) || a("<div>").attr("un", g), oParent:this})), this._moChildren[g] && !1 !== this.switchChild(this._msActiveChild, g) && (h.shift(), this._moChildren[g].onhashchange(h.join("/") || g, f))) : this._msActiveChild && this.switchChild(this._msActiveChild, null);
        return this
    }, switchChild:function() {
    }}).Inherit({popupWindow:function(b, c, e, f, h) {
            var g = this.getDom$();
            g.html(a.tmpl("popupwindow")).find(".content").html(c);
            g.find(".header p").html(b);
            d.widget.screenCentral(g, a.extend({rawPosDom$:e, offset:f, showMask:!0, lightMask:!0}, h));
            g.draggable({handle:".header", cursor:"move"})
        }, showTips:function(b, c, e) {
            var f = a("#tips");
            f.find(".tipsDesc").html(b);
            f.find(".tipsIcon")[c ? "removeClass" : "addClass"]("errorIcon");
            d.widget.screenCentral(f, a.extend({showMask:!1, adjustPos:!1}, e));
            setTimeout(function() {
                f.hide()
            }, 1500)
        }, alert:function(b, a, c) {
            this._showTips(b || "", a, !0, !1, c)
        }, confirm:function(b, a, c) {
            this._showTips(b || "", a, !0, !0, c)
        }, closeAlertOrConfirm:function() {
            a("#redirectDialog").hide()
        }, _showTips:function(b, c, e, f, h) {
            var g = a("#redirectDialog"), q = g.find(".dialogContent"), b = a("<div></div>").html(b);
            q.html(b.addClass(h ? h : "default"));
            d.widget.screenCentral(g.show());
            c = a.extend({ok:function() {
            }, cancel:function() {
            }}, c);
            g.find("[un='ok']").off("click").on("click", function() {
                g.hide();
                c.ok(q)
            })[e ? "show" : "hide"]()[f ? "removeClass" : "addClass"]("singleBtn");
            g.find("[un='cancel']").off("click").on("click", function() {
                g.hide();
                c.cancel(q)
            })[f ? "show" : "hide"]();
            g.off("keydown").on("keydown", function(b) {
                a.isHotkey(b, "enter") ? (g.hide(), c.ok(q)) : a.isHotkey(b, "esc") ? (g.hide(), c.cancel(q)) : b.stopPropagation()
            })
        }, onhashchange:function(b, a) {
            a && a.addClass("active");
            this.Root.onhashchange.call(this, b)
        }, switchChild:function(b, a) {
            var c = b && b != a && this._moChildren[b].getDom$(), d = a && this._moChildren[a].getDom$();
            if(b != a && (c && c.hide(), d && d.show(), b && this._moChildren[b])) {
                this._moChildren[b]._mbActive = !1;
                this._moChildren[b]._inactive();
                c = 0;
                for(d = this._moChildren[b]._moComponets.length;c < d;c++) {
                    this._moChildren[b]._moComponets[c]._inactive()
                }
            }
            (this._msActiveChild = a) && this._moChildren[a] && (this._moChildren[a]._mbActive = !0);
            return!0
        }})}, g = {};
    a.extend(d || {}, {createCtrl:function() {
        var b = 2 == arguments.length && ["base"].concat([].slice.apply(arguments)) || arguments;
        h[b[1]] = (h[b[0]] || h.base).Inherit(b[2])
    }, ctrl:function(b, a) {
        return g[b] = h[b] && new h[b](b, a) || {}
    }, getCtrlInstants:function(b) {
        return g[b]
    }, ctrlComponents:function(c, d) {
        var e = [], f;
        for(f in h) {
            if(0 == f.indexOf(c.getName() + "_")) {
                var g = a.extend({}, d, {oDom$:b(f, c.getDom$()) || a("<div>").attr("un", f)});
                e.push(this.ctrl(f, g))
            }
        }
        return e
    }});
    d.widget = {}
})(jQuery, WebMM, this);
(function(a, d) {
    function f() {
        for(var b = [], d = 0, f = c.length;d < f;d++) {
            b.push("type=" + c[d].Type)
        }
        d = {BaseRequest:{Uin:0, Sid:0}, Count:c.length, List:c};
        a.netQueue("statReport").send("/cgi-bin/mmwebwx-bin/webwxstatreport?" + b.join("&"), d);
        clearTimeout(e);
        e = 0;
        c = []
    }
    var c = [], e;
    d.WebMM = a.extend(d.WebMM || {}, {ossLog:function(b) {
        b = a.extend({Type:1}, b);
        !c.length && 0 == e && (e = setTimeout(f, 6E4));
        c.push(b);
        10 <= c.length && f()
    }, flushOssLog:function() {
        f()
    }})
})(jQuery, this);
(function(a, d, f, c) {
    function e(c, e) {
        if(b <= c) {
            if(a.isFunction(e[0])) {
                a.safe(function() {
                    e[0]()
                });
                return
            }
            var i = "";
            try {
                i = d.model("account").getUserInfo().Uin
            }catch(j) {
                i = "Can't get."
            }
            for(var i = {Type:1, Text:JSON.stringify(e), Uin:i, Date:(new Date).getTime()}, l = 0;l < e.length;l++) {
                f.WebLog = a.formatDate(new Date, "hh:mm:ss") + "\n" + JSON.stringify(e[l]) + "\n\n" + f.WebLog
            }
            WebMM.ossLog(i)
        }
        d.vConsole && d.vConsole.print(c, e)
    }
    f.WebLog = "";
    var b = 1;
    f.Log = {level:function(a) {
        if(a == c) {
            return b
        }
        b = a
    }, i:function() {
        e(0, arguments)
    }, d:function() {
        e(1, arguments)
    }, w:function() {
        e(2, arguments)
    }, e:function() {
        e(3, arguments)
    }};
    f.onerror = function(b, a, c) {
        var e = {Type:2, Text:JSON.stringify({msg:b, line:c, url:a, func:arguments.callee.caller})};
        WebMM.ossLog(e);
        d.vConsole && d.vConsole.print(3, [e]);
        return!1
    };
    f.debug = Log.d
})(jQuery, WebMM, this);
(function(a, d, f) {
    function c(b) {
        if(!b) {
            return!1
        }
        var a = j[0], c = a.getAttribute("step");
        null == c && (c = 0);
        "right" == b ? 3 == c ? c = 0 : c++ : "left" == b && (0 == c ? c = 3 : c--);
        a.setAttribute("step", c);
        if(document.all) {
            switch(a.style.filter = "progid:DXImageTransform.Microsoft.BasicImage(rotation=" + c + ")", c) {
                case 0:
                    a.parentNode.style.height = a.height;
                    break;
                case 1:
                    a.parentNode.style.height = a.width;
                    break;
                case 2:
                    a.parentNode.style.height = a.height;
                    break;
                case 3:
                    a.parentNode.style.height = a.width
            }
        }else {
            l = document.getElementById("canvas_pop_img");
            null == l && (l = document.createElement("canvas"), l.setAttribute("id", "canvas_pop_img"), a.parentNode.appendChild(l));
            b = l.getContext("2d");
            a.style.visibility = "hidden";
            a.style.position = "absolute";
            switch(c) {
                default:
                    ;
                case 0:
                    l.setAttribute("width", a.width);
                    l.setAttribute("height", a.height);
                    b.rotate(0 * Math.PI / 180);
                    b.drawImage(a, 0, 0);
                    break;
                case 1:
                    l.setAttribute("width", a.height);
                    l.setAttribute("height", a.width);
                    b.rotate(90 * Math.PI / 180);
                    b.drawImage(a, 0, -a.height);
                    break;
                case 2:
                    l.setAttribute("width", a.width);
                    l.setAttribute("height", a.height);
                    b.rotate(180 * Math.PI / 180);
                    b.drawImage(a, -a.width, -a.height);
                    break;
                case 3:
                    l.setAttribute("width", a.height), l.setAttribute("height", a.width), b.rotate(270 * Math.PI / 180), b.drawImage(a, -a.width, 0)
            }
            l.style.display = "block"
        }
    }
    function e(b, c) {
        var d = b.offset(), e = b.width(), j = b.height(), m = a(f).width(), n = a(f).height(), C = m / 1.5, A = n / 1.5, v = c[0].width, y = c[0].height, w = 2 * v, F = 2 * y, B = v / y, E = m / n;
        if(v > C || y > A) {
            B >= E ? (v = C, y = v / B) : (y = A, v = B * y)
        }
        var G = v / 2, u = y / 2, z = {left:(m - v) / 2, top:(n - y) / 2, width:v, height:y};
        c.width(e).height(j);
        l && (l.style.display = "none");
        c.css("width", "100%").css("height", "100%").css("left", "0");
        var x = c.parent();
        x.css({left:d.left, top:d.top, width:e, height:j}).show().animate(z, 500, "swing", function() {
            h.open().find('[opt="download"]').attr("url", i + "&fun=download");
            g == null && (g = x.find(".iconClose"));
            g.show().off("click").on("click", function() {
                g.hide();
                h.close();
                x.hide();
                a("#mask").off("click").stop().animate({opacity:0}, function() {
                    a("#mask").hide()
                })
            });
            var b = 1;
            k = function(a, c) {
                debug(a);
                debug(x.width());
                debug(x.height());
                debug(G);
                debug(u);
                if(!(a > 0 && (x.width() > w || x.height() > F))) {
                    if(!(a < 0 && (x.width() < G || x.height() < u))) {
                        b = b + 0.2 * a;
                        b < 0.5 && (b = 0.5);
                        var d = z.width, e = z.height;
                        z.width = v * b;
                        z.height = y * b;
                        z.left = parseInt(x.css("left")) - (z.width - d) * (c.offsetX / d || 0.5);
                        z.top = parseInt(x.css("top")) - (z.height - e) * (c.offsetY / e || 0.5);
                        x.css(z)
                    }
                }
            };
            c.bind("mousewheel", function(b, a) {
                k(Math.abs(a) / a, b)
            })
        })
    }
    var b = a("#slidePic"), h = a("#popImgOperator"), g = null, i, j, l, k, m;
    h.off("click").on("click", function(b) {
        var b = b.target, a = b.getAttribute("opt");
        if("zoomOut" == a) {
            k(2, {offsetX:0, offsetY:0})
        }else {
            if("zoomIn" == a) {
                k(-2, {offsetX:0, offsetY:0})
            }else {
                if("rotateLeft" == a) {
                    c("left")
                }else {
                    if("rotateRight" == a) {
                        c("right")
                    }else {
                        if("download" == a) {
                            var d = f.onbeforeunload;
                            f.onbeforeunload = null;
                            b.getAttribute("url") && (location.href = b.getAttribute("url"));
                            setTimeout(function() {
                                f.onbeforeunload = d
                            })
                        }
                    }
                }
            }
        }
    }).bind({mouseenter:function() {
            h.appear()
        }, mouseleave:function() {
            h.disappear()
        }});
    h.open = function() {
        var b = this;
        b.show().css({opacity:1});
        m = setTimeout(function() {
            b.animate({opacity:0})
        }, 3E3);
        b.on = !0;
        return b
    };
    h.close = function() {
        clearTimeout(m);
        this.on = !1;
        this.hide();
        return this
    };
    h.appear = function() {
        h.on && (m && clearTimeout(m), h.stop(!0, !0).animate({opacity:1}))
    };
    h.disappear = function() {
        h.on && (m && clearTimeout(m), m = setTimeout(function() {
            h.stop(!0, !0).animate({opacity:0})
        }, 1E3))
    };
    b.delegate("img", "mouseenter", h.appear).delegate("img", "mouseleave", h.disappear);
    d.popImage = function(c, d) {
        var f = new Image;
        f.onload = function() {
            b.find("img").remove();
            b = b.append(f);
            c.removeWaitEffect();
            a("#mask").css("opacity", 0).show().stop().animate({opacity:0.6}, function() {
                e(c, j = a(f))
            }).off("click").on("click", function() {
                    h.close();
                    b.stop().hide();
                    a("#mask").off("click").stop().animate({opacity:0}, function() {
                        a("#mask").hide()
                    });
                    g.hide()
                });
            b.draggable({handle:"img"})
        };
        f.onerror = function() {
            c.removeWaitEffect()
        };
        c.insertWaitEffect();
        i = f.src = d
    };
    var n = {};
    d.widget = a.extend(d.widget || {}, {preLoadImg:function(b, c) {
        if(b && !n[b]) {
            var d = new Image;
            d.onload = d.onerror = d.onabort = function() {
                n[this.src] && n[this.src].callback && a.safe(n[this.src].callback);
                delete n[this.src]
            };
            d.src = b;
            n[d.src] = {img:d, callback:c}
        }
    }, replaceImg:function(b) {
        Log.d(b)
    }})
})(jQuery, WebMM, this);
(function(a) {
    a.fn = a.extend(a.fn, {insertWaitEffect:function() {
        var d = a(a("#waitingEffect")[0].cloneNode(!0)).show().appendTo(this.parent());
        d.css({left:(this[0].clientWidth - d[0].width) / 2, top:(this[0].clientHeight - d[0].height) / 2});
        return this
    }, removeWaitEffect:function() {
        this.parent().find("#waitingEffect").remove();
        return this
    }})
})(jQuery, WebMM, this);
(function(a) {
    a.millTimeFormator = function(a, f) {
        function c(b, a) {
            var c = new Date(b);
            c.setUTCHours(15, 59, 59, 999);
            return e - (c.getTime() - a)
        }
        if(0 > +a || 0 > +f) {
            return""
        }
        var e = 1E3 * +f, b = 1E3 * +a, h = e - b, g = {"\ufffd\u0578\ufffd":{max:6E4, unit:1E3}, "nn\ufffd\ufffd\ufffd\ufffd\u01f0":{max:36E5, unit:6E4}, "nn\u0421\u02b1\u01f0":{max:216E5, unit:36E5}, "\ufffd\ufffd\ufffd\ufffd hh:mm":{max:c(e, 864E5), unit:864E5}, "\ufffd\ufffd\ufffd\ufffd hh:mm":{max:c(e, 1728E5), unit:864E5}, "MM\ufffd\ufffddd\ufffd\ufffd hh:mm":{max:function(b) {
            b = new Date(b);
            b.setFullYear(b.getFullYear(), 0, 1);
            b.setUTCHours(-8, 0, 0, 0);
            return e - b.getTime()
        }(e), unit:864E5}, "yyyy/MM/dd hh:mm":{max:Infinity, unit:0}}, i;
        for(i in g) {
            var j = g[i];
            if(j.max > h) {
                var b = new Date(b), g = b.getHours() + "", l = b.getMinutes() + "", g = 1 == g.length ? "0" + g : g, l = 1 == l.length ? "0" + l : l;
                return 0 != j.unit ? i.replace("nn", Math.floor(h / j.unit)).replace("hh", g).replace("mm", l).replace("MM", b.getMonth() + 1).replace("dd", b.getDate()) : i.replace("yyyy", b.getFullYear()).replace("MM", b.getMonth() + 1).replace("dd", b.getDate()).replace("hh", g).replace("mm", l)
            }
        }
    }
})(jQuery);
(function(a, d, f) {
    var c = {onplay:function() {
        Log.d("jPlayer play")
    }, onprogress:function() {
        Log.d("jPlayer progress")
    }, onpause:function() {
        Log.d("jPlayer pause")
    }, onstop:function() {
        Log.d("jPlayer ended")
    }}, e = null, b = null, h = null;
    _oVideoJPlayerContainer$ = null;
    d.setMediaPlayerUICallbacks = function(b) {
        a.extend(c, c, b)
    };
    d.getMediaPlayer = function() {
        return e
    };
    d.widget.playNewMsgSound = function(a) {
        b && (b.jPlayer("setMedia", {mp3:b.attr("url" + a)}), b.jPlayer("play"))
    };
    a(function() {
        setTimeout(function() {
            e || (e = a("#mediaPlayer").jPlayer({ready:function() {
                Log.d("jPlayer ready")
            }, play:function(b) {
                c.onplay(b)
            }, progress:function(b) {
                c.onprogress(b)
            }, pause:function(b) {
                c.onpause(b)
            }, stop:function(b) {
                c.onstop(b)
            }, ended:function(b) {
                c.onstop(b)
            }, swfPath:d.getRes("swf_jplayer"), supplied:"mp3", solution:"flash, html", wmode:"window"}))
        }, 500);
        setTimeout(function() {
            b || (b = a("#newMsgPlayer").jPlayer({ready:function() {
            }, play:function() {
            }, progress:function() {
            }, pause:function() {
            }, stop:function() {
            }, ended:function() {
            }, swfPath:d.getRes("swf_jplayer"), supplied:"mp3", solution:"flash, html", wmode:"window"}))
        }, 500);
        h || setTimeout(function() {
            _oVideoJPlayerContainer$ = a("#videoPlayerContainer");
            h = a("#jquery_jplayer_1").jPlayer({ready:function() {
                Log.d("jPlayer ready")
            }, play:function() {
                Log.d("jPlayer play")
            }, progress:function() {
                Log.d("jPlayer progress")
            }, pause:function() {
                Log.d("jPlayer pause")
            }, stop:function() {
                Log.d("jPlayer stop")
            }, ended:function() {
                Log.d("jPlayer ended")
            }, swfPath:d.getRes("swf_jplayer"), supplied:"flv, m4v", solution:"flash, html", size:{width:"766px", height:"360px", cssClass:"jp-video-360p"}});
            _oVideoJPlayerContainer$.bind("click", function(b) {
                b = a(b.target);
                b.hasClass("ico_close_circle") ? (h.jPlayer("stop"), _oVideoJPlayerContainer$.hide(), a("#mask").off("click").stop().animate({opacity:0}, function() {
                    a("#mask").hide()
                })) : b.hasClass("jp-download-screen")
            }).draggable({handle:".jp_header", cursor:"move"});
            _oVideoJPlayerContainer$.find(".jp-download-screen").click(function() {
                var b = f.onbeforeunload;
                f.onbeforeunload = null;
                location.href = g.download;
                setTimeout(function() {
                    f.onbeforeunload = b
                })
            });
            h.jPlayer("play")
        }, 0)
    });
    var g = null;
    d.playVideo = function(b) {
        a("#mask").css("opacity", 0).show().stop().animate({opacity:0.6}).off("click").on("click", function() {
            h.jPlayer("stop");
            _oVideoJPlayerContainer$.hide();
            a("#mask").off("click").stop().animate({opacity:0}, function() {
                a("#mask").hide()
            })
        });
        d.widget.screenCentral(_oVideoJPlayerContainer$.show());
        h.jPlayer("stop");
        h.jPlayer("setMedia", g = b);
        setTimeout(function() {
            h.jPlayer("play")
        }, b.flv ? 1E3 : 0)
    }
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = null;
    d.widget = a.extend(d.widget || {}, {filterQQFace:function(a, b) {
        c = c || f.gQQFaceMap;
        b || (a = a.replace(/\[([^\]]+)\]/g, function(b, a) {
            var e;
            return(e = c[a]) ? '<img src="' + d.getRes("img_path") + "qqface/" + e + '.png" />' : b
        }));
        for(var h = a.length - 1, g, i;0 <= h;) {
            if("/" == a[h]) {
                for(var j = 0;4 > j;j++) {
                    if(i = c[g = a.substr(h + 1, j)]) {
                        a = a.substring(0, h) + (!b ? '<img src="' + d.getRes("img_path") + "/qqface/" + i + '.png" />' : "[" + g + "]") + a.substring(h + j + 1);
                        break
                    }
                }
            }
            h--
        }
        return a
    }, preFilterEmoji:function(a) {
        return a = a.replace(/<.*?>/g, function(b) {
            return c[b] ? b.replace("<", "{").replace(">", "}") : b
        })
    }, afterFilterEmoji:function(a) {
        return a = a.replace(/{.*?}/g, function(b) {
            var a;
            return(a = c[b.replace("{", "<").replace("}", ">")]) ? '<span class="emoji emoji' + a + '"></span>' : b
        })
    }, afterEncodeEmoji:function(a) {
        var a = a.replace(/{.*?}/g, function(b) {
            var a;
            return(a = c[b.replace("{", "<").replace("}", ">")]) ? f.gEmojiCodeMap[a] || "" : b
        }), b;
        for(b in gEmojiCodeConv) {
            for(;0 <= a.indexOf(b);) {
                a = a.replace(b, gEmojiCodeConv[b])
            }
        }
        return a
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = {"44682e637b75a3f5d6747d61dbd23a15":"icon_001.gif", c0059fa4f781a2a500ec03fade10e9b1:"icon_002.gif", "86cb157e9c44b2c9934e4e430790776d":"icon_006.gif", e6f269a19ff2fb61fdb847b39c86ebca:"icon_007.gif", ea675fef6e28b0244c4577c6d5a2e5c9:"icon_009.gif", d629cb3c544fb719405f2b9f16ed6e6c:"icon_010.gif", e2e2e96798bfbd55b35c3111d89b2e17:"icon_012.gif", d13e21be9fd71777f727e0c34b0d3994:"icon_013.gif", "68f9864ca5c0a5d823ed7184e113a4aa":"icon_018.gif", "1483ce786912099e29551915e0bc2125":"icon_019.gif",
        bb82ce58f5ed6fdd2b5e34fc2a8e347a:"icon_020.gif", "31574013280aac3897722cc7e3e49ee4":"icon_021.gif", a00d1de64298d9eaa145ec848a9cc8af:"icon_022.gif", "6257411b26d5aa873762490769625bb9":"icon_024.gif", "5a7fc462d63ef845e6d99c1523bbc91e":"icon_027.gif", "3a4dc10bc33c74726f46ba1eacd97391":"icon_028.gif", "72ebfa527add152c6872219044b151c3":"icon_029.gif", "6a9284bc5ce0bf059375e970a49fa2c5":"icon_030.gif", "2c4597ce27b24af08652be6bea644c32":"icon_033.gif", "6ae79b62bab61132981f1e85ad7070c4":"icon_035.gif",
        aab84584b5a3f262286cb38bb107b53e:"icon_040.gif"}, c = {"icon_001.gif":"44682e637b75a3f5d6747d61dbd23a15", "icon_002.gif":"c0059fa4f781a2a500ec03fade10e9b1", "icon_006.gif":"86cb157e9c44b2c9934e4e430790776d", "icon_007.gif":"e6f269a19ff2fb61fdb847b39c86ebca", "icon_009.gif":"ea675fef6e28b0244c4577c6d5a2e5c9", "icon_010.gif":"d629cb3c544fb719405f2b9f16ed6e6c", "icon_012.gif":"e2e2e96798bfbd55b35c3111d89b2e17", "icon_013.gif":"d13e21be9fd71777f727e0c34b0d3994", "icon_018.gif":"68f9864ca5c0a5d823ed7184e113a4aa",
        "icon_019.gif":"1483ce786912099e29551915e0bc2125", "icon_020.gif":"bb82ce58f5ed6fdd2b5e34fc2a8e347a", "icon_021.gif":"31574013280aac3897722cc7e3e49ee4", "icon_022.gif":"a00d1de64298d9eaa145ec848a9cc8af", "icon_024.gif":"6257411b26d5aa873762490769625bb9", "icon_027.gif":"5a7fc462d63ef845e6d99c1523bbc91e", "icon_028.gif":"3a4dc10bc33c74726f46ba1eacd97391", "icon_029.gif":"72ebfa527add152c6872219044b151c3", "icon_030.gif":"6a9284bc5ce0bf059375e970a49fa2c5", "icon_033.gif":"2c4597ce27b24af08652be6bea644c32",
        "icon_035.gif":"6ae79b62bab61132981f1e85ad7070c4", "icon_040.gif":"aab84584b5a3f262286cb38bb107b53e"};
    d.widget = a.extend(d.widget || {}, {parseTuzki:function(c) {
        var c = (a.htmlDecode(c) || "").split("<br/>"), c = a.xml2json(1 < c.length ? c[1] : c[0]), b;
        return c && c.emoji.androidmd5 && (b = f[c.emoji.androidmd5]) ? d.getRes("img_path") + "/emoji/" + b : ""
    }, getTuzkiMd5:function(a) {
        return c[a]
    }, getTuzkiPath:function(a) {
        return d.getRes("img_path") + "/emoji/" + a
    }, getTuzkiPathByMd5:function(a) {
        return this.getTuzkiPath(f[a])
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = null;
    a(window).resize(function() {
        c && c.isShow() && d.widget.screenCentral(c)
    });
    d.widget.screenCentral = function(d, b) {
        if(d && d.length) {
            if(!b || !1 !== b.adjustPos) {
                c = d
            }
            if(b && b.rawPosDom$) {
                var h = b.rawPosDom$.offset(), g = b.rawPosDom$.width(), i = b.rawPosDom$.height(), j = d.width(), l = d.height();
                d.css({left:h.left, top:h.top, position:"absolute", width:g, height:i});
                d.animate({left:(a(document.body).width() - j) / 2 + (b.offset && b.offset.left || 0), top:(a(document.body).height() - l) / 2 + a(f).scrollTop() + (b.offset && b.offset.top || 0), position:"absolute", width:j, height:l})
            }else {
                d.css({left:(d.offsetParent().innerWidth() - d.outerWidth()) / 2 + (b && b.offset && b.offset.left || 0), top:((f.innerHeight || document.documentElement.clientHeight) - d.outerHeight()) / 2 + a(f).scrollTop(), position:"absolute"})
            }
            if(b && b.showMask) {
                if(a("#mask").css("opacity", 0).show().stop().animate({opacity:b.lightMask ? 0 : 0.6}, function() {
                    d.show()
                }), b.clickMaskHide) {
                    a("#mask").off("click").on("click", function() {
                        d.hide();
                        a("#mask").off("click").stop().animate({opacity:0}, function() {
                            a("#mask").hide()
                        });
                        b.onhide && b.onhide()
                    })
                }
            }else {
                d.fadeIn("fast")
            }
            return d
        }
    }
})(jQuery, WebMM, this);
(function(a) {
    function d(a) {
        return(a || "").toLowerCase().split("+").sort().join("").replace(/\s/ig, "")
    }
    var f = {27:"esc", 9:"tab", 32:"space", 13:"enter", 8:"backspace", 145:"scroll", 20:"capslock", 144:"numlock", 19:"pause", 45:"insert", 36:"home", 46:"del", 35:"end", 33:"pageup", 34:"pagedown", 37:"left", 38:"up", 39:"right", 40:"down", 107:"=", 109:"-", 112:"f1", 113:"f2", 114:"f3", 115:"f4", 116:"f5", 117:"f6", 118:"f7", 119:"f8", 120:"f9", 121:"f10", 122:"f11", 123:"f12", 188:"<", 190:">", 191:"/", 192:"`", 219:"[", 220:"\\", 221:"]", 222:"'"}, c = {"`":"~", 1:"!", 2:"@", 3:"#", 4:"$", 5:"%",
        6:"^", 7:"&", 8:"*", 9:"(", "0":")", "-":"_", "=":"+", ";":":", "'":'"', ",":"<", ".":">", "/":"?", "\\":"|"};
    a.isHotkey = function(a, b) {
        var h, g = a.keyCode;
        h = f[g];
        if(!(g = !h && 49 <= g && 90 >= g && String.fromCharCode(g).toLowerCase())) {
            if(g = a.type, g = "mousewheel" == g || "DOMMouseScroll" == g) {
                g = 0 < a.wheelDelta || 0 > a.detail ? "mousewheelup" : "mousewheeldown"
            }
        }
        var i = a.ctrlKey, j = a.shiftKey, l = a.altKey, k = j && (c[g] || c[h]), m = [];
        !i && (!l && k) && (h = k, j = g = null);
        i && m.push("ctrl");
        j && m.push("shift");
        l && m.push("alt");
        h && m.push(h);
        g && m.push(g);
        h = m.join("+");
        return d(h) == d(b)
    }
})(jQuery, this);
(function(a, d, f) {
    function c() {
        return g || (g = QMActivex.create(b))
    }
    function e(b, a) {
        var e = i || (i = QMActivex.create(h));
        e.StopUpload();
        e.ClearHeaders();
        e.ClearFormItems();
        e && (e.URL = d.getRes("url_host") + "/cgi-bin/mmwebwx-bin/webwxpreview?fun=upload", e.AddHeader("Cookie", document.cookie), e.AddFormItem("msgimgrequest", 0, 0, b), e.AddFormItem("filename", 1, 4, !c() || !c() || !c().IsClipBoardImage ? !1 : c().SaveClipBoardBmpToFile(1)), e.OnEvent = function(b, c) {
            switch(c) {
                case 3:
                    e && (a(JSON.parse(e.Response)), e = null);
                    break;
                case 1:
                    Log.d("screensnap upload error"), a({}), e = null
            }
        }, e.StartUpload())
    }
    var b = "screencapture", h = "uploader", g = null, i = null;
    d.widget.screenSnap = {isSupport:function() {
        return f.QMActivex && 0 < QMActivex.isSupport(b)
    }, install:function() {
        window.open(QMActivex.installUrl.replace(/^https/, "http"))
    }, capture:function(b) {
        var a = c();
        a && (a.OnCaptureFinished = b.ok);
        a.OnCaptureCanceled = function() {
        };
        a.DoCapture()
    }, isClipBoardImage:function() {
        return c() && c().IsClipBoardImage
    }, upload:function(b, a) {
        if(c() && c().IsClipBoardImage) {
            return e(b, a), !0
        }
    }}
})(jQuery, WebMM, this);
(function(a) {
    var d = 0;
    a.textAreaResize = function(f, c, e, b) {
        var h = a(f), g = c || h.height(), i = e || h.height();
        !h.attr("defHeight") && h.height("defHeight", h.height());
        f.onkeydown = f.onkeyup = f.onchange = f.onpropertychange = null;
        if(0 > g || 0 > i) {
            h.height(h.attr("defHeight"))
        }else {
            var j = f.parentNode.appendChild(f.cloneNode(!0));
            with(j.style) {
                visibility = "hidden", position = "absolute", left = "-1000px", paddingBottom = paddingTop = "0px", paddingLeft = h.css("paddingLeft"), paddingRight = h.css("paddingRight"), width = h.width() + "px", overflow = "hidden"
            }
            f.onkeydown = f.onkeyup = f.onfocus = f.onblur = f.onchange = function() {
                j.style.width = h.width() + "px";
                j.value = f.value;
                var a = j.scrollHeight, c = h.height();
                0 < a && (a != d && c != a) && (d = a, f.style.height = (a < g ? g : a > i ? i : a) + "px", f.style.overflow = a > i ? "auto" : "hidden", b && h.height() != c && b(h.height() - c))
            }
        }
    }
})(jQuery, WebMM, this);
(function(a, d) {
    d.widget = a.extend(d.widget || {}, {scrollFocus:function(a, c, d, b) {
        if(a && a.size() && c && c.size()) {
            var h = a.scrollTop(), g = h + a.parent().height(), i = c.position().top, j = i + c.height(), l = 0;
            h > i ? l = i - 20 : g < j && (l = h + j - g + 20);
            0 != l && b ? (a.scrollTop(l), d.css("top", c.position().top - a.scrollTop() + c.height() / 2 - 20)) : d.stop().animate({top:c.position().top - a.scrollTop() + c.height() / 2 - 20}, "fast")
        }
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    function c(b, c, d, e) {
        var f = [], h = [], g = [], e = e || {}, i = a.browser.msie ? '<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" <#=codebase#> <#=attr#> <#=id#> ><#=param#></object>' : '<embed <#=embed#> type="application/x-shockwave-flash" <#=pluginspage#>  <#=name#> <#=id#> ></embed>';
        e.allowscriptaccess = d && d.allowscriptaccess || "always";
        e.quality = "high";
        for(var l in e) {
            var j = {name:l, value:e[l]};
            h.push(a.tmpl('<param name="<#=name#>" value="<#=value#>" />', j));
            g.push(a.tmpl(" <#=name#>=<#=value#> ", j))
        }
        for(l in d) {
            j = {name:l, value:d[l]}, f.push(a.tmpl(" <#=name#>=<#=value#> ", j)), g.push(a.tmpl(" <#=name#>=<#=value#> ", j))
        }
        c && (h.push(a.tmpl('<param name="<#=name#>" value="<#=value#>" />', {name:"movie", value:c})), g.push(a.tmpl(" <#=name#>=<#=value#> ", {name:"src", value:c})));
        return a.tmpl(i, {id:b && [' id="', b, '"'].join(""), name:b && [' name="', b, '"'].join(""), attr:f.join(""), param:h.join(""), embed:g.join(""), codebase:"https:" == location.protocol ? "" : 'codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" ', pluginspage:"https:" == location.protocol ? "" : 'pluginspage="http://www.adobe.com/cn/products/flashplayer" '})
    }
    function e(b, a) {
        var c = a || window;
        return(c = c[b] || c.document[b]) && (c.length ? c[c.length - 1] : c)
    }
    function b(b) {
        if(!(this._mId = b.id)) {
            throw Error(0, "config.id can't use null");
        }
        if(!(this._mWin = b.win)) {
            throw Error(0, "config.win win is null");
        }
        this._mFlash = b.flash;
        this._moConstructor = this.constructor;
        this._mEvent = b;
        this._initlize()
    }
    function h(e, h) {
        var n = a.extend({onbefore:function() {
        }, onprocess:function() {
        }, onsuccess:function() {
        }, onerror:function() {
        }, oncomplete:function() {
        }}, h);
        if(e && 0 != e.size()) {
            var q = a.tmpl(j, {height:e.height(), width:e.width(), margin:0, code:c(g, d.getRes("swf_uploader") + "?r=" + a.now(), {width:"100%", height:"100%"}, {wmode:"transparent"})});
            a("#swfUploaderWrapper").remove();
            e.prepend(q);
            clearTimeout(l);
            l = 0;
            l = setTimeout(function() {
                (new b({id:g, win:f, onSelect:function(b, a) {
                    for(var c = b;c <= a;c++) {
                        n.onselect(c, {name:i.getFileInfo(c, "name"), size:parseInt(i.getFileInfo(c, "size"), 10)})
                    }
                }, onProcess:function(b, a) {
                    n.onprocess(b, a);
                    n.onsuccess()
                }, onError:function(b, a, c, d) {
                    n.onerror(a, c, d)
                }, onComplete:function(b, a) {
                    n.oncomplete(b, a)
                }})).setup(function(b, a) {
                        b ? (i = this.getFlash(), i.initlize("single"), i.clearUploadVars(), i.addUploadVar("timeout", 6E4)) : Log.e("the flash uploader is not ok..." + a)
                    })
            }, 300)
        }
    }
    a.getFlash = e;
    _goStatic = b;
    _goClass = _goStatic.prototype;
    _goStatic.get = function(b, a) {
        var c = a[this._CONST._CACHES];
        return c && c[b]
    };
    _goStatic.getFlashVer = function() {
        var b = "", a = -1, c = -1, d = -1, e = navigator.plugins;
        if(e && e.length) {
            for(var f = 0, h = e.length;f < h;f++) {
                var g = e[f];
                if(-1 != g.name.indexOf("Shockwave Flash")) {
                    b = g.description.split("Shockwave Flash ")[1];
                    a = parseFloat(b);
                    d = parseInt(b.split("r")[1]);
                    c = parseInt(b.split("b")[1]);
                    break
                }
            }
        }else {
            try {
                if(f = new ActiveXObject("ShockwaveFlash.ShockwaveFlash")) {
                    b = f.GetVariable("$version").split(" ")[1], h = b.split(","), a = parseFloat(h.join(".")), d = parseInt(h[2]), c = parseInt(h[3])
                }
            }catch(i) {
            }
        }
        return{version:(isNaN(a) ? -1 : a) || -1, build:(isNaN(d) ? -1 : d) || -1, beta:(isNaN(c) ? -1 : c) || -1, desc:b}
    };
    _goStatic.isSupported = function() {
        var b = this.getFlashVer();
        return 10 <= b.version || 9 == b.version && 50 < b.build
    };
    _goStatic._CONST = {_TIMEOUT:5E3, _CACHES:"qmFlashCaches_ASDr431gGas", _CALLBACK:"onFlashEvent_ASDr431gGas"};
    _goClass.getFlash = function() {
        return this._mFlash || e(this._mId, this._mWin)
    };
    _goClass.isDisabled = function() {
        return this._mDisabled || !1
    };
    _goClass.disable = function(b) {
        this._mDisabled = !1 != b;
        return this
    };
    _goClass.setup = function(a) {
        function c(b, e) {
            try {
                a.call(d, b, e)
            }catch(f) {
            }
        }
        var d = this;
        this._getLoadedPercent(function(a) {
            100 == a ? setTimeout(function() {
                try {
                    if(!d.getFlash().setup(b._CONST._CALLBACK, d._mId)) {
                        return c(!1, "setuperr")
                    }
                }catch(a) {
                    return c(!1, "nosetup")
                }
                c(!0)
            }) : "number" != typeof a && c(!1, a)
        })
    };
    _goClass._getLoadedPercent = function(c) {
        function d(b) {
            try {
                c.call(e, b)
            }catch(a) {
            }
        }
        var e = this, f = this.getFlash();
        if(!f) {
            return d("notfound")
        }
        var h = 0;
        (function() {
            var c = arguments.callee;
            c._startTime || (c._startTime = a.now());
            var e = 0, g = !1;
            try {
                e = f.PercentLoaded()
            }catch(i) {
                g = !0
            }
            e != h && d(h = e);
            100 != e && (a.now() - c._startTime > b._CONST._TIMEOUT ? d(g ? "noflash" : "timeout") : setTimeout(c, 100))
        })()
    };
    _goClass._initlize = function() {
        var b = this._mWin, a = this._moConstructor._CONST, c = a._CACHES, a = a._CALLBACK;
        b[c] || (b[c] = new b.Object);
        b[c][this._mId] = this;
        b[a] || (b[a] = function() {
            var a = arguments[1], d = b[c][arguments[0]];
            if(d && "function" == typeof d._mEvent[a]) {
                for(var e = [], f = 2, h = arguments.length;f < h;f++) {
                    e.push(arguments[f])
                }
                d._mEvent[a].apply(d, e)
            }
        })
    };
    var g = "flashUploader", i = null, j = '<span id="swfUploaderWrapper" style="top:0;left:0;position:absolute;width:100%;height:<#=height#>px;margin:<#=margin#>;z-index:2;"><#=code#></span>', l = 0;
    d.widget = a.extend(d.widget || {}, {swfUploader:{isSupport:function() {
        return b.isSupported()
    }, install:function(b, a) {
        h(b, a)
    }, upload:function(b, a, c) {
        i.setUploadUrl(a);
        for(var d in c) {
            i.addUploadVar(d, c[d])
        }
        i.upload(b, "filename", !1)
    }}})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = {ondisplay:function() {
    }, onerror:function() {
    }, onclose:function() {
    }, onclick:function() {
    }}, e = null;
    f.MMNotification = d.widget.notification = {notify:function(b, d, f, i) {
        if(this.isSupport()) {
            var i = a.extend(c, i), j = i.onclick, l = window.webkitNotifications;
            i.onclick = function() {
                e && (j.apply(this, arguments), e.cancel(), e = null)
            };
            0 == l.checkPermission() ? (e && (e.cancel(), e = null), e = l.createNotification(b, d, f), a.extend(e, i), setTimeout(function() {
                if(e) {
                    e.show();
                    clearTimeout(0);
                    setTimeout(function() {
                        if(e) {
                            e.cancel();
                            e = null
                        }
                    }, 1E4)
                }
            })) : l.checkPermission()
        }
    }, cancel:function() {
        e && (e.cancel(), e = null)
    }, requestPermission:function() {
        if(this.isSupport()) {
            var b = window.webkitNotifications;
            1 == b.checkPermission() && b.requestPermission(function() {
            })
        }
    }, checkPermission:function() {
        return this.isSupport() ? f.webkitNotifications.checkPermission() : 2
    }, isSupport:function() {
        return!!f.webkitNotifications
    }}
})(jQuery, WebMM, this);
(function(a, d, f) {
    function c(c) {
        var j = a.extend({onReady:function() {
        }, onRecordStart:function() {
        }, onRecordError:function() {
        }, onRecordStop:function() {
        }, onRecordFinish:function() {
        }, onSendError:function() {
        }, onSendProgress:function() {
        }, onSendFinish:function() {
        }, onActivityTime:function() {
        }, onSecurityPanelClose:function() {
        }}, c), c = a.tmpl(g, {WrapID:e, code:a.generateFlashCode(b, d.getRes("swf_recorder"), {width:"100%", height:"100%"}, {wmode:"transparent"})});
        a("#" + e).remove();
        a(document.body).append(c);
        clearTimeout(i);
        i = setTimeout(function() {
            (new a.qmFlash(a.extend(j, {id:b, win:f}))).setup(function(b, a) {
                b ? (h = this.getFlash(), j.onReady()) : Log.e("the flash recorder is not ok..." + a)
            })
        }, 300)
    }
    var e = "VoiceRecorderWrapper", b = "VoiceRecorder", h = null, g = '<div id="<#=WrapID#>" style="top:0px;left:-1000px;position:absolute;width:300px;height:200px;z-index:9999;"><#=code#></div>', i = 0, j = !1;
    d.widget = a.extend(d.widget || {}, {Recorder:{isSupport:function() {
        return a.qmFlash.isSupported()
    }, install:function(b) {
        if(j) {
            b.onReady()
        }else {
            c(b), j = !0
        }
    }, getObject:function() {
        return h
    }}})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = a("#uploadPreview");
    f.uploadPreview = {show:function() {
        c.find("img").replaceWith(a("<img/>").attr("src", d.getRes("img_loading1")));
        d.widget.screenCentral(c.show());
        return this
    }, hide:function() {
        c.hide();
        a("#mask").hide();
        return this
    }, getDom$:function() {
        return c
    }, setImg:function(a) {
        var b = new Image;
        b.onload = function() {
            var a = c.find(".picPreviewWrap"), d = a.find("img"), e = a.width(), a = a.height(), f = this.width, l = this.height;
            if(f > e || l > a) {
                f / l > e / a ? (b.style.width = e + "px", b.style.height = e * l / f + "px") : (b.style.height = a + "px", b.style.width = f * a / l + "px")
            }
            d.replaceWith(b)
        };
        b.src = a;
        return this
    }, setCallback:function(d) {
        var b = this;
        c.off("click").on("click", function(c) {
            c = a(c.target).attr("opt");
            "cancel" == c ? (b.hide(), d.cancel && d.cancel()) : "send" == c && d.send && (b.hide(), d.send())
        });
        return this
    }}
})(jQuery, WebMM, this);
(function(a, d, f) {
    function c(b) {
        var c = a(document.body), f = e.ctrl("root", {oDom$:c}), h = b || "chat";
        f.dispatch("hashchange", "root/" + (a.hash() || h));
        a.hashChange(function(b) {
            b = b || h;
            f.dispatch("hashchange", "root/" + b)
        });
        var g = {};
        d.globalEventSetting = function(b) {
            return a.extend(g, b || {})
        };
        c.bind("click keyup keydown change", function(b) {
            for(var c = !1, e = !1, h = b.target, i = b.type, l = [];h && h != document.body;) {
                h.getAttribute(i) && l.push(h), h = h.parentNode
            }
            h = 0;
            i = l.length;
            a:for(;h < i;h++) {
                var j = a(l[h]);
                if(!g.globalIntercept || a.contains(g.interceptDom$[0], j[0])) {
                    for(var k = j.parents("[ctrl]"), m = j.attr(b.type), n = m && m.split("@"), p = n && n[0], n = n && n[1], E = 0, G = k.length;m && E < G;E++) {
                        var u = k[E].ctrl;
                        if(u[p] && (u = u[p](b, j, n && j.parents(n).first()), c = !0, !1 === u)) {
                            break a
                        }
                    }
                    "A" == j.prop("tagName") && "javascript:;" == j.prop("href") && (e = !0)
                }
            }
            c || (c = "click" == b.type && "noHandledClick" || "keydown" == b.type && "noHandledKeyDown" || "keyup" == b.type && "noHandledKeyUp") && f.dispatch("globalevent", {type:c, data:b});
            e || "A" == b.target.tagName && "javascript:;" == b.target.href || "A" == b.target.parentNode.tagName && "javascript:;" == b.target.parentNode.href ? (b.stopPropagation(), b.preventDefault()) : "A" == b.target.tagName && (0 == b.target.href.indexOf("http") && "" == b.target.target) && (window.open(b.target.href), b.stopPropagation(), b.preventDefault());
            d.touchUserAction()
        }).bind("globalevent", function(b, a) {
                f.dispatch("globalevent", a)
            })
    }
    var e = f.WebMM = f.WebMM || {}, b = {};
    e.getRes = function(a) {
        return b[a]
    };
    var h = null;
    e.getDeviceId = function() {
        if(!h) {
            h = "e";
            for(var b = 0;15 > b;b++) {
                h += Math.floor(10 * Math.random())
            }
        }
        return h
    };
    d.timeoutDetect = function(b) {
        return"1100" == b ? (f.onbeforeunload = null, d.util.logout(0), !0) : "1101" == b ? (f.onbeforeunload = null, d.util.logout(1), !0) : !1
    };
    a.netQueueSetting({globalExceptionHandler:function(b) {
        return d.timeoutDetect(b)
    }});
    var g = !0, i = 0;
    d.touchUserAction = function() {
        g || d.triggerEvent("hasUserAction", g = !0);
        i = a.now()
    };
    setInterval(function() {
        3E4 < a.now() - i && d.triggerEvent("hasUserAction", g = !1)
    }, 3E4);
    d.touchUserAction();
    f.GlobalConfig && f.GlobalConfig.gRes && (b = GlobalConfig.gRes, f.Log.level(GlobalConfig.gLog), f.GlobalRes = null);
    var j = !1, l;
    f.ready = function(b) {
        if(b == "view" || f.viewReady) {
            j = true
        }
        b == "js" && (l = true);
        if(j && l) {
            a.getTmplStr = function(b) {
                return document.getElementById("viewFrame").contentWindow.document.getElementById(b).innerHTML
            };
            c()
        }
    };
    var k = {check:function() {
        a.qmFlash.isSupported() || Log.e("Not Support Flash. Navigator: " + f.Navigator)
    }};
    a(function() {
        ready("js");
        k.check()
    });
    d.ErrOk = 0;
    d.ErrSessionTimeOut = 1;
    d.ErrNet = 2;
    d.ErrFail = 3
})(jQuery, WebMM, this);
(function(a, d) {
    var f = "weibo qqmail fmessage tmessage qmessage qqsync floatbottle lbsapp shakeapp medianote qqfriend readerapp blogapp facebookapp masssendapp meishiapp feedsapp voip blogappweixin weixin brandsessionholder weixinreminder wxid_novlwrv3lqwv11 gh_22b87fa7cb3c".split(" "), c = ["wxid_novlwrv3lqwv11", "gh_22b87fa7cb3c"];
    d.util = a.extend(d.util || {}, {isSpUser:function(a) {
        for(var b = 0, c = f.length;b < c;b++) {
            if(f[b] === a || a.endsWith("@qqim")) {
                return!0
            }
        }
        return!1
    }, isShieldUser:function(a) {
        if(/@lbsroom/.test(a)) {
            return!0
        }
        for(var b = 0, d = c.length;b < d;++b) {
            if(c[b] == a) {
                return!0
            }
        }
        return!1
    }, isFileHelper:function(a) {
        return a == d.Constants.SP_CONTACT_FILE_HELPER
    }, isRoomContact:function(a) {
        if(!a) {
            return!1
        }
        var b = a.lastIndexOf("@chatroom");
        return 0 > b ? !1 : b == a.length - 9
    }, isTalkContact:function(a) {
        if(!a) {
            return!1
        }
        var b = a.lastIndexOf("@talkroom");
        return 0 > b ? !1 : b == a.length - 9
    }, getMsgPeerUserName:function(a) {
        return a.isSend ? a.ToUserName : a.FromUserName
    }, getMediaTypeCode:function() {
    }, getContactDisplayName:function(c) {
        if("string" === a.type(c) && (c = d.model("contact").getContact(c), null == c)) {
            return c
        }
        var b = "";
        if(!c || !c.UserName) {
            return b
        }
        if(d.util.isRoomContact(c.UserName)) {
            if(b = c.RemarkName || c.NickName, !b && c.MemberList) {
                for(var f = 0, g = c.MemberList.length;f < g;++f) {
                    0 < b.length && (b += ", ");
                    var i = c.MemberList[f], j = d.model("contact").getContact(i.UserName), b = b + (j && (j.RemarkName || j.NickName) || i.NickName || i.UserName)
                }
            }else {
                b || (b = c.UserName)
            }
        }else {
            b = c.RemarkName || c.NickName || c.UserName
        }
        c.orderC = a.clearHtmlStr(c.RemarkPYQuanPin || c.PYQuanPin || c.NickName || c.UserName || "").toLocaleUpperCase().replace(/\W/ig, "");
        "A" > c.orderC.charAt(0) && (c.orderC = "~");
        return b
    }, isImgMsg:function(a) {
        return a == d.Constants.MM_DATA_IMG || a == d.Constants.MM_DATA_PRIVATEMSG_IMG || a == d.Constants.MM_DATA_QQLIXIANMSG_IMG
    }, isTextMsg:function(a) {
        switch(a) {
            case d.Constants.MM_DATA_TEXT:
                ;
            case d.Constants.MM_DATA_PRIVATEMSG_TEXT:
                ;
            case d.Constants.MM_DATA_QMSG:
                return!0;
            default:
                return!1
        }
    }, isVoiceMsg:function(a) {
        return a == d.Constants.MM_DATA_VOICEMSG
    }, isVideoMsg:function(a) {
        return a == d.Constants.MM_DATA_VIDEO || a == d.Constants.MM_DATA_VIDEO_IPHONE_EXPORT
    }, isSysMsg:function(a) {
        return a == d.Constants.MM_DATA_SYS
    }, isEmojiMsg:function(a) {
        return a == d.Constants.MM_DATA_EMOJI
    }, isQqMailMsg:function(a) {
        return a == d.Constants.MM_DATA_APPMSG
    }, isQqMsg:function(a) {
        return a == d.Constants.MM_DATA_QMSG
    }, isPushSystmeMsg:function(a) {
        return a == d.Constants.MM_DATA_PUSHSYSTEMMSG
    }, isRecommendAssistant:function(a) {
        return a == d.Constants.MM_DATA_POSSIBLEFRIEND_MSG || a == d.Constants.MM_DATA_VERIFYMSG
    }, isAppMsg:function(a) {
        return a == d.Constants.MM_DATA_APPMSG
    }, genMessageDigest:function(a) {
        var b = "";
        _nMsgType = a.MsgType;
        if(-9999 == _nMsgType) {
            b = ""
        }else {
            var b = this.isTextMsg(_nMsgType) || _nMsgType == d.Constants.MM_DATA_READER_TYPE ? a.digest : this.isImgMsg(_nMsgType) ? d.getRes("text_image_msg") : this.isVoiceMsg(_nMsgType) ? d.getRes("text_voice_msg") : this.isVideoMsg(_nMsgType) ? d.getRes("text_video_msg") : this.isEmojiMsg(_nMsgType) ? d.getRes("text_emoji_msg") : _nMsgType == d.Constants.MM_DATA_APP_MSG_EMOJI_TYPE ? d.getRes("text_emoji_msg") : this.isAppMsg(_nMsgType) || _nMsgType >= d.Constants.MM_DATA_APP_MSG_IMG_TYPE ? d.getRes("text_app_msg") :
                a.digest, c = "";
            if(this.isRoomContact(a.FromUserName) && (a = d.model("contact").getContact(a.actualSender))) {
                c = d.util.getContactDisplayName(a), c += c && ": " || ""
            }
            b = b && c + b || ""
        }
        return b.replace(/<br\/?>/ig, " ")
    }, isBrandContact:function(a) {
        return a & d.Constants.MM_USERATTRVERIFYFALG_BIZ_BRAND
    }, getRoomMsgActualSender:function(a) {
        var b = a.Content.indexOf(":");
        return 0 > b ? "" : a.Content.substr(0, b)
    }, isSelf:function(a) {
        return d.model("account").getUserName() == a
    }, modifyNickName:function(a) {
        if(a) {
            switch(a.UserName) {
                case "weixin":
                    a.NickName = d.getRes("text_weixin_nickname");
                    break;
                case "filehelper":
                    a.NickName = d.getRes("text_filehelper_nickname");
                    break;
                case "newsapp":
                    a.NickName = d.getRes("text_newsapp_nickname");
                    break;
                case "fmessage":
                    a.NickName = d.getRes("text_fmessage_nickname");
                    break;
                case "gh_8f619b5732ed":
                    a.NickName = d.getRes("tencent_2012_2_sessions")
            }
        }
    }, isContact:function(a) {
        return(a = d.model("contact").getContact(a)) && a.isContact && a.isContact()
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = {hasPhotoAlbum:function() {
        return this.SnsFlag & 1
    }}, c = [], e = null, b = null, h = "", g = "";
    d.model("account", {getSyncKey:function() {
        return e || {}
    }, setSyncKey:function(b) {
        b ? e = b : Log.e("JS Function: setSyncKey. Error. no synckey")
    }, getSid:function() {
        return b || (b = a.getCookie("wxsid"))
    }, setSid:function(a) {
        a && (b = a)
    }, getSkey:function() {
        return h
    }, setSkey:function(b) {
        b && (h = b)
    }, setUserInfo:function(b) {
        b ? (a.extend(f, b), f.isMute = this.isMute(), f.isNotifyOpen = this.isNotifyOpen(), d.triggerEvent("accountUpdated", f)) : Log.e("JS Function: setUserInfo. Error. no accout")
    }, getUserInfo:function() {
        return f && f.UserName && f || null
    }, getUin:function() {
        return this.getUserInfo() && this.getUserInfo().Uin || a.getCookie("wxuin")
    }, getUserName:function() {
        return this.getUserInfo() && this.getUserInfo().UserName
    }, getBaseRequest:function() {
        return{BaseRequest:{Uin:this.getUin(), Sid:this.getSid(), Skey:this.getSkey(), DeviceID:d.getDeviceId()}}
    }, reset:function() {
    }, setHistoryConversation:function(b) {
        c = c.concat(b.split(",")) || [];
        d.addEventListener("messageAdded", function(b) {
            for(var b = b.UserName, a = 0, d = c.length;a < d;a++) {
                c[a] == b && c.splice(a, 1)
            }
        })
    }, getHistoryConversation:function() {
        return c
    }, isMute:function() {
        return this.getUserInfo().WebWxPluginSwitch & d.Constants.MM_WEBWXFUNCTION_TONE_NOT_OPEN
    }, isGroupMute:function() {
        return!1
    }, setMute:function(b) {
        f.WebWxPluginSwitch = b ? f.WebWxPluginSwitch | d.Constants.MM_WEBWXFUNCTION_TONE_NOT_OPEN : f.WebWxPluginSwitch & ~d.Constants.MM_WEBWXFUNCTION_TONE_NOT_OPEN;
        f.isMute = this.isMute();
        return this
    }, isNotifyOpen:function() {
        return this.getUserInfo().WebWxPluginSwitch & d.Constants.MM_WEBWXFUNCTION_NOTIFY_OPEN
    }, setNotifyOpen:function(b) {
        f.WebWxPluginSwitch = b ? f.WebWxPluginSwitch | d.Constants.MM_WEBWXFUNCTION_NOTIFY_OPEN : f.WebWxPluginSwitch & ~d.Constants.MM_WEBWXFUNCTION_NOTIFY_OPEN;
        f.isNotifyOpen = this.isNotifyOpen();
        return this
    }, isHigherVer:function() {
        return 4.5 <= g
    }, setClientVer:function(b) {
        b = parseInt(b, 10).toString(16);
        b.substr(0, 1);
        g = b = b.substr(1, 3).replace("0", ".")
    }});
    d.model("account").reset()
})(jQuery, WebMM, this);
(function(a, d) {
    _oContacts = {};
    _oReverseMap = {};
    var f = {isSelf:function() {
        return d.model("account").getUserName() == this.UserName
    }, isContact:function() {
        return!!(this.ContactFlag & d.Constants.MM_CONTACTFLAG_CONTACT)
    }, isBlackContact:function() {
        return!!(this.ContactFlag & d.Constants.MM_CONTACTFLAG_BLACKLISTCONTACT)
    }, isConversationContact:function() {
        return!!(this.ContactFlag & d.Constants.MM_CONTACTFLAG_CHATCONTACT)
    }, isRoomContact:function() {
        return this.UserName.endsWith("@chatroom")
    }, isRoomContactDel:function() {
        return this.isRoomContact() && !(this.ContactFlag & d.Constants.MM_CONTACTFLAG_CHATROOMCONTACT)
    }, isRoomOwner:function() {
        return this.isRoomContact() && this.OwnerUin == d.model("account").getUin()
    }, isBrandContact:function() {
        return this.VerifyFlag & d.Constants.MM_USERATTRVERIFYFALG_BIZ_BRAND
    }, isSpContact:function() {
        return d.util.isSpUser(this.UserName)
    }, isShieldUser:function() {
        return d.util.isShieldUser(this.UserName)
    }, isFileHelper:function() {
        return this.UserName == d.Constants.SP_CONTACT_FILE_HELPER
    }, isRecommendHelper:function() {
        return"fmessage" == this.UserName
    }, isNewsApp:function() {
        return this.UserName == d.Constants.SP_CONTACT_NEWSAPP
    }, isMuted:function() {
        return this.Statues === d.Constants.MM_CHATROOM_NOTIFY_CLOSE && this.isRoomContact()
    }, _canSearchMemberList:function(a) {
        if(this.isRoomContact()) {
            for(var e = 0, b = this.MemberList.length;e < b;e++) {
                var f = this.MemberList[e].UserName;
                if((f = d.model("contact").getContact(f)) && f.canSearch(a)) {
                    return!0
                }
            }
        }
    }, canSearch:function(a, d) {
        if(!a) {
            return this.weight = 1, !0
        }
        var a = a.toUpperCase(), b = 0, f = 0, b = this.RemarkName.toUpperCase().indexOf(a), f = this.RemarkPYQuanPin.toUpperCase().indexOf(a);
        if(0 <= b || 0 <= f) {
            return this.weight = 0 == b ? 1 : 0 == f ? 0.9 : 0.6, !0
        }
        b = this.NickName.toUpperCase().indexOf(a);
        f = this.PYQuanPin.toUpperCase().indexOf(a);
        return 0 <= b || 0 <= f ? (this.weight = 0 == b ? 0.8 : 0 == f ? 0.7 : 0.4, !0) : 0 <= this.Alias.toUpperCase().indexOf(a) || 0 <= this.UserName.toUpperCase().indexOf(a) || d && this.isRoomContact() && this._canSearchMemberList(a) ? (this.weight = 0.5, !0) : !1
    }, update:function(c) {
        c && (a.extend(this, c), d.triggerEvent("contactUpdated", this))
    }, hasPhotoAlbum:function() {
        return this.SnsFlag & 1
    }};
    d.model("contact", {addContacts:function(a, e) {
        if(a) {
            for(var b = 0, f = a.length;b < f;b++) {
                this.addContact(a[b])
            }
            e || d.triggerEvent("contactListReady")
        }
    }, addContact:function(c) {
        if(c && !d.util.isShieldUser(c.UserName)) {
            var e = "";
            d.util.modifyNickName(c);
            "fmessage" == c.UserName && (c.ContactFlag = 0);
            if(_oContacts[c.UserName]) {
                if(0 === c.ContactFlag) {
                    this.deleteContact(c.UserName);
                    return
                }
                d.util.isRoomContact(c.UserName) && 0 == c.MemberCount && (delete c.MemberCount, delete c.MemberList);
                a.extend(_oContacts[c.UserName], c);
                e = "contactUpdated"
            }else {
                _oContacts[c.UserName] = c, e = "contactAdded"
            }
            if(d.util.isRoomContact(c.UserName) && 0 < c.MemberCount) {
                for(var b = 0, h = c.MemberList.length;b < h;b++) {
                    var g = c.MemberList[b];
                    _oReverseMap[g.UserName] || (_oReverseMap[g.UserName] = []);
                    _oReverseMap[g.UserName].push(c.Uin)
                }
            }
            h = _oContacts[c.UserName];
            h.DisplayName = d.util.getContactDisplayName(h);
            b = _oContacts;
            c = c.UserName;
            h = a.extend({RemarkPYQuanPin:"", RemarkPYInitial:"", PYInitial:"", PYQuanPin:""}, h, f);
            h.avatar = d.util.getNormalAvatarUrl(h.UserName);
            h = b[c] = h;
            d.triggerEvent(e, h)
        }
    }, getContact:function(a) {
        return _oContacts[a] || null
    }, isContactExisted:function(a) {
        return!!_oContacts[a]
    }, getAllContacts:function() {
        return _oContacts
    }, getAllStarContact:function(a) {
        var d = [], a = a || {}, b;
        for(b in _oContacts) {
            var f = _oContacts[b];
            !f.isSelf() && (1 == f.StarFriend && !a[b]) && d.push(f)
        }
        return d = d.sort(function(b, a) {
            return b.orderC > a.orderC ? 1 : -1
        })
    }, getAllChatroomContact:function() {
        var a = [], d;
        for(d in _oContacts) {
            var b = _oContacts[d];
            b.isRoomContact() && a.push(b)
        }
        return a = a.sort(function(b, a) {
            return b.orderC > a.orderC ? 1 : -1
        })
    }, getAllFriendChatroomContact:function(a) {
        var d = [], b;
        for(b in _oContacts) {
            var f = _oContacts[b];
            f.isContact() && (f.isRoomContact() && f.canSearch(a)) && d.push(f)
        }
        return d = d.sort(function(b, a) {
            return b.orderC > a.orderC ? 1 : -1
        })
    }, getAllBrandContact:function() {
        var a = [], d;
        for(d in _oContacts) {
            var b = _oContacts[d];
            b.isContact() && b.isBrandContact() && a.push(b)
        }
        return a = a.sort(function(b, a) {
            return b.orderC > a.orderC ? 1 : -1
        })
    }, getAllFriendContact:function(a, e, b, f) {
        var g = [], b = b || {}, i;
        for(i in _oContacts) {
            if(!b[i]) {
                var j = _oContacts[i];
                j.isSelf() && !d.model("account").isHigherVer() || (!j.isContact() || e && 1 == j.StarFriend || j.isRoomContact() || f && j.isBrandContact() || j.isShieldUser()) || j.canSearch(a) && g.push(j)
            }
        }
        return g = g.sort(function(b, a) {
            return b.orderC > a.orderC ? 1 : -1
        })
    }, getAllCanChatContactUserName:function(a) {
        var e = [], b;
        for(b in _oContacts) {
            var f = _oContacts[b];
            (f.isSelf() && d.model("account").isHigherVer() || (f.isContact() || f.isRoomContact() || f.isSpContact()) && !f.isShieldUser()) && f.canSearch(a, !0) && e.push(b)
        }
        return e
    }, deleteContact:function(c) {
        a.isArray(c) || (c = [c]);
        for(var e = 0, b = c.length;e < b;e++) {
            var f = c[e], g = null;
            if(g = _oContacts[f]) {
                delete _oContacts[f], d.triggerEvent("contactDeleted", g)
            }
        }
    }, getContactCount:function() {
        var a = 0, d;
        for(d in _oContacts) {
            a++
        }
        return a
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = {}, c = {}, e = {};
    d.model("photoalbum", {getByUserName:function(b) {
        return f[b]
    }, setByUserName:function(b, a) {
        f[b] = a;
        this._setCurrentIdByUserName(b, a.ObjectList);
        20 > a.ObjectList.length && this.setLoadAllByUserName(b)
    }, addByUserName:function(b, a) {
        var c = f[b];
        c ? this._setCurrentIdByUserName(b, a.ObjectList) && (c.NewRequestTime = a.NewRequestTime, 0 != a.ObjectList.length && (c.ObjectCount += a.ObjectCount, c.ObjectCountForSameMd5 += a.ObjectCountForSameMd5, c.ObjectList = c.ObjectList.concat(a.ObjectList)), 20 > a.ObjectList.length && this.setLoadAllByUserName(b)) : this.setByUserName(b, a)
    }, getAlbumStateByUserName:function(a) {
        c[a] || (c[a] = {currentId:0, loadAll:!1});
        return c[a]
    }, _setCurrentIdByUserName:function(a, c) {
        var d = c.length, e = this.getAlbumStateByUserName(a);
        if(1 > d) {
            return e.currentId = 0, !0
        }
        d = c[d - 1].Id;
        if(e.currentId == d) {
            return!1
        }
        e.currentId = d;
        this.setMediaListByUserName(a, c);
        return!0
    }, getCurrentIdByUserName:function(a) {
        return this.getAlbumStateByUserName(a).currentId
    }, setLoadAllByUserName:function(a) {
        this.getAlbumStateByUserName(a).loadAll = !0
    }, getLoadAllByUserName:function(a) {
        return this.getAlbumStateByUserName(a).loadAll
    }, setMediaListByUserName:function(a, c) {
        if(!(1 > c.length)) {
            var d = this.getMediaListByUserName(a), f;
            f = 1 > d.length ? 0 : d[d.length - 1].albumIndex + 1;
            for(var j = 0, l = c.length;j < l;++j) {
                for(var k = c[j].ObjectDesc.ContentObject.mediaList.media, m = 0, n = k.length;m < n;++m) {
                    var q = k[m];
                    q.albumIndex = f + j;
                    q.photoIndex = m;
                    q.thumb = "/cgi-bin/mmwebwx-bin/webwxgetpubliclinkimg?pictype=sns&url=" + q.thumb;
                    q.url = "/cgi-bin/mmwebwx-bin/webwxgetpubliclinkimg?pictype=sns&url=" + q.url
                }
                d = d.concat(k)
            }
            e[a] = d
        }
    }, getMediaListByUserName:function(a) {
        e[a] || (e[a] = []);
        return e[a]
    }})
})(jQuery, WebMM, this);
(function(a, d, f, c) {
    function e(a, b) {
        for(var c = 0;c < a.length;++c) {
            if(a[c].MsgId == b) {
                return c
            }
        }
        return-1
    }
    function b(a) {
        if(!a) {
            return""
        }
        var b = a.MsgType, c = d.util;
        return c.isTextMsg(b) || c.isSysMsg(b) || b == d.Constants.MM_DATA_READER_TYPE || b == d.Constants.MM_DATA_APP_MSG_TEXT_TYPE || b == d.Constants.MM_DATA_VERIFYMSG || b == d.Constants.MM_DATA_SHARECARD || b == d.Constants.MM_DATA_POSSIBLEFRIEND_MSG ? c.isRoomContact(a.FromUserName) ? (b = a.Content.indexOf(":<br/>"), 0 > b ? a.Content : a.Content.substr(b + 6)) : a.Content : d.Constants.MM_DATA_APPMSG_UNSUPPORT == b ? d.getRes("text_chatmsglist_app_msg_unspport") : d.Constants.MM_DATA_LOCATION ==
            b ? d.getRes("text_location_msg") : d.Constants.MM_DATA_VOIPMSG == b || d.Constants.MM_DATA_VOIPNOTIFY == b || d.Constants.MM_DATA_VOIPINVITE == b ? d.getRes("text_voip_msg") : d.getRes("text_chatmsglist_msg_unspport")
    }
    var h = {}, g = null, i = {isSysMessage:function() {
        return this.MsgType == d.Constants.MM_DATA_SYS
    }, update:function(b) {
        b && (a.extend(this, b), d.triggerEvent("messageUpdated", this))
    }};
    d.addEventListener("accountUpdated", function(a) {
        var b = d.model("account").getUserName();
        if(a = a.avatar) {
            for(var c in h) {
                for(var e = h[c], f = 0, g = e.length;f < g;++f) {
                    e[f].avatarId && e[f].avatarId == b && (e[f].avatar = a)
                }
            }
        }
    });
    d.model("message", {getMessages:function(a) {
        return h[a] ? h[a] : []
    }, getUnreadMsgsCount:function(a) {
        var b = 0;
        if(a = h[a]) {
            for(var c = a.length - 1;0 <= c;c--) {
                a[c].unread && ++b
            }
        }
        return b
    }, markMsgsRead:function(a) {
        for(var a = this.getMessages(a), b = !1, c = 0, d = a.length;c < d;c++) {
            a[c].unread && (b = !0), a[c].unread = !1
        }
        return b
    }, getFirstMessage:function(a) {
        a = this.getMessages(a);
        return a.length && a[0] || null
    }, getLastMessage:function(a) {
        a = this.getMessages(a);
        return a.length && a[a.length - 1] || {}
    }, getMsgById:function(a, b) {
        var c = this.getMessages(a), d = e(c, b);
        return 0 <= d ? c[d] : null
    }, getMsgByLocalId:function(a, b) {
        var c;
        a: {
            for(var d = this.getMessages(a), e = 0;e < d.length;++e) {
                if(d[e].LocalID == b) {
                    c = d[e];
                    break a
                }
            }
        }
        return c
    }, getNextUnreadVoiceMsg:function(a, b) {
        for(var c = this.getMessages(a), e = !1, f = 0, g = c.length;f < g;f++) {
            if(!e && c[f].MsgId == b) {
                e = !0
            }else {
                if(e && c[f].MsgType == d.Constants.MM_DATA_VOICEMSG && c[f].Status == d.Constants.STATE_REACH) {
                    return c[f]
                }
            }
        }
        return null
    }, addFakeSysMsg:function(b) {
        this.addMessages([{MsgId:a.now(), MsgType:b.MsgType, FromUserName:b.FromUserName, ToUserName:b.ToUserName, Status:d.Constants.STATE_SENT, CreateTime:b.CreateTime || a.now() / 1E3, Content:b.Content, unread:!1}])
    }, initMessageQueue:function(b, c) {
        if(b && !d.util.isShieldUser(b)) {
            if(h[b]) {
                return!1
            }
            h[b] = [];
            var e = d.util.isFileHelper(b) && 0 == h[b].length ? 1E4 : -9999, f = 0 < e ? d.getRes("text_file_helper_tip") : "", c = 0 < e ? a.now() / 1E3 : c;
            this.addMessages([{MsgId:a.now(), MsgType:e, FromUserName:"", ToUserName:b, Status:d.Constants.STATE_SENT, CreateTime:c ? c : a.now() / 1E3, Content:f, unread:!1}]);
            return!0
        }
    }, getQueueUserNames:function() {
        var a = [], b;
        for(b in h) {
            a.push(b)
        }
        return a
    }, addMessages:function(f, l) {
        if(f) {
            a.isArray(f) || (f = [f]);
            for(var k = 0, m = f.length;k < m;k++) {
                try {
                    var n = f[k], q = n.FromUserName, p = n.ToUserName, s, o = n;
                    g || (g = d.model("account").getUserName());
                    o.isSend = o.FromUserName == g || "" == o.FromUserName;
                    s = o.isSend ? o.ToUserName : o.FromUserName;
                    var r = h[s] || (h[s] = []);
                    Log.d("msgid=" + n.MsgId);
                    n.actualSender = d.util.isRoomContact(q) ? d.util.getRoomMsgActualSender(n) : q;
                    if(!(n.MsgType == d.Constants.MM_DATA_STATUSNOTIFY || d.util.isTalkContact(q) || d.util.isTalkContact(p) || d.util.isShieldUser(q) || d.util.isShieldUser(p) || n.MsgType == d.Constants.MM_DATA_VERIFYMSG && n.RecommendInfo && n.RecommendInfo.UserName == d.model("account").getUserInfo().UserName)) {
                        var D;
                        D = e(r, n.MsgId);
                        if(0 > D) {
                            var t = b(n);
                            n.LocalID != c && n.LocalID == n.ClientMsgId && (t = d.widget.preFilterEmoji(t), t = a.htmlEncode(t), t = t.replace(/\n/g, "<br/>"), t = d.widget.afterFilterEmoji(t));
                            n.LocalID || (n.ClientMsgId = n.LocalID = n.MsgId);
                            n.digest = a.clearLinkTag(d.widget.filterQQFace(t));
                            n.actualContent = a.hrefEncode(d.widget.filterQQFace(t));
                            n.FromUserName != d.model("account").getUserName() && (n.unread == c && n.MsgType != d.Constants.MM_DATA_SYS) && (n.unread = !0);
                            if(n.MsgType == d.Constants.MM_DATA_VERIFYMSG) {
                                var C = n.RecommendInfo.UserName, A;
                                a: {
                                    for(o = 0;o < r.length;++o) {
                                        var v = r[o];
                                        if(v.MsgType == d.Constants.MM_DATA_VERIFYMSG && v.RecommendInfo.UserName == C) {
                                            A = o;
                                            break a
                                        }
                                    }
                                    A = -1
                                }
                                if(0 > A) {
                                    n.History = ["0" + n.RecommendInfo.Content]
                                }else {
                                    var y = r[A];
                                    y.History.push("0" + n.RecommendInfo.Content);
                                    n.History = y.History
                                }
                            }
                            n.avatarTitle = a.htmlEncode(a.clearHtmlStr(d.util.getContactDisplayName(n.actualSender)));
                            n.avatarId = n.actualSender;
                            n.avatar = d.util.getNormalAvatarUrl(n.actualSender, n.FromUserName);
                            if(l === c) {
                                var w = r[r.length - 1];
                                if((o = n) && !(0 > o.MsgType)) {
                                    if(!w || 0 > w.MsgType) {
                                        var F = new Date(1E3 * o.CreateTime);
                                        o.displayTime = o.CreateTime;
                                        o.time = F.getHours() + ":" + a.formatNum(F.getMinutes(), 2)
                                    }else {
                                        var B = new Date(1E3 * o.CreateTime);
                                        180 <= Math.abs(w.displayTime - o.CreateTime) ? (o.displayTime = o.CreateTime, o.time = B.getHours() + ":" + a.formatNum(B.getMinutes(), 2)) : (o.displayTime = w.displayTime, o.time = "")
                                    }
                                }
                                r.push(n)
                            }else {
                                r.splice(l, 0, n)
                            }
                            a.extend(n, i);
                            d.triggerEvent(l === c ? "messageAdded" : "messagePrepend", n)
                        }else {
                            this.updateMessage(r, D, n)
                        }
                    }
                }catch(E) {
                    Log.e("JS Function: addMessages. try catch error: " + E)
                }
            }
        }
    }, updateMessage:function(b, c, e) {
        a.extend(b[c], e);
        d.triggerEvent("messageUpdated", e)
    }, deleteMessage:function(a) {
        h[a] && (delete h[a], d.triggerEvent("sessionDeleted", a))
    }})
})(jQuery, WebMM, this);
(function(a, d, f, c) {
    var e = {};
    d.model("history", {inputRecord:function(a, d) {
        return d != c && (e[a] = d) || e[a] || ""
    }, getAll:function() {
        return e
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.Constants = a.extend(d.Constants || {}, {MM_DATA_TEXT:1, MM_DATA_HTML:2, MM_DATA_IMG:3, MM_DATA_PRIVATEMSG_TEXT:11, MM_DATA_PRIVATEMSG_HTML:12, MM_DATA_PRIVATEMSG_IMG:13, MM_DATA_VOICEMSG:34, MM_DATA_PUSHMAIL:35, MM_DATA_QMSG:36, MM_DATA_VERIFYMSG:37, MM_DATA_PUSHSYSTEMMSG:38, MM_DATA_QQLIXIANMSG_IMG:39, MM_DATA_POSSIBLEFRIEND_MSG:40, MM_DATA_SHARECARD:42, MM_DATA_VIDEO:43, MM_DATA_VIDEO_IPHONE_EXPORT:44, MM_DATA_EMOJI:47, MM_DATA_LOCATION:48, MM_DATA_APPMSG:49, MM_DATA_VOIPMSG:50, MM_DATA_STATUSNOTIFY:51,
        MM_DATA_VOIPNOTIFY:52, MM_DATA_VOIPINVITE:53, MM_DATA_SYSNOTICE:9999, MM_DATA_SYS:1E4, MM_DATA_READER_TYPE:10001, MM_DATA_APP_MSG_TEXT_TYPE:10002, MM_DATA_APP_MSG_IMG_TYPE:10003, MM_DATA_APP_MSG_AUDIO_TYPE:10004, MM_DATA_APP_MSG_VIDEO_TYPE:10005, MM_DATA_APP_MSG_URL_TYPE:10006, MM_DATA_APP_MSG_ATTACH_TYPE:10007, MM_DATA_APP_MSG_OPEN_TYPE:10008, MM_DATA_APP_MSG_EMOJI_TYPE:10009, MM_DATA_APPMSG_UNSUPPORT:65585, MM_MEDIA_TYPE_IMAGE:1, MM_MEDIA_TYPE_VIDEO:2, MM_MEDIA_TYPE_AUDIO:3, MM_MEDIA_TYPE_ATTACHMENT:4,
        SP_CONTACT_FILE_HELPER:"filehelper", SP_CONTACT_NEWSAPP:"newsapp", MMWEBWX_JSLOG:1, MMWEBWX_JSERR:2, MMWEBWX_WEBSESSIONTIMEOUT_LOGOUT:4, MMWEBWX_CONNECT_ERR:5, MMWEBWX_USETIME:6, MMWEBWX_LOGIN_COSTTIME:7, MMWEBWX_NEW_CHAT:9, MMWEBWX_UPLOADMEDIA_TOO_LARGE:11, MMWEBWX_GETVOICE:12, STATE_UNKNOWN:0, STATE_SENDING:1, STATE_SENT:2, STATE_REACH:3, STATE_READ:4, STATE_FAILED:5, APPMSGTYPE_TEXT:1, APPMSGTYPE_IMG:2, APPMSGTYPE_AUDIO:3, APPMSGTYPE_VIDEO:4, APPMSGTYPE_URL:5, APPMSGTYPE_ATTACH:6, APPMSGTYPE_OPEN:7,
        APPMSGTYPE_EMOJI:8, APPMSGTYPE_VOICE_REMIND:9, MM_APPMSG_SHOW_DEFAULT:0, MM_APPMSG_SHOW_READER:1, MM_APPMSG_SHAKETRANIMG_RESULT:2, MM_APPMSG_VOICEREMIND_CONFIRM:3, MM_APPMSG_VOICEREMIND_REMIND:4, MM_APPMSG_VOICEREMIND_SYS:5, MM_BIZ_DATA_TEXT:1, MM_BIZ_DATA_IMG:2, MM_BIZ_DATA_VOICE:3, MM_BIZ_DATA_VIDEO:4, MM_BIZ_DATA_APPMSG:10, MM_BIZ_DATA_SHARECARD:42, MM_CONTACTFLAG_CONTACT:1, MM_CONTACTFLAG_CHATCONTACT:2, MM_CONTACTFLAG_CHATROOMCONTACT:4, MM_CONTACTFLAG_BLACKLISTCONTACT:8, MM_CONTACTFLAG_DOMAINCONTACT:16,
        MM_CONTACTFLAG_HIDECONTACT:32, MM_CONTACTFLAG_FAVOURCONTACT:64, MM_CONTACTFLAG_3RDAPPCONTACT:128, MM_CONTACTFLAG_SNSBLACKLISTCONTACT:256, MM_USERATTRVERIFYFALG_BIZ:1, MM_USERATTRVERIFYFALG_FAMOUS:2, MM_USERATTRVERIFYFALG_BIZ_BIG:4, MM_USERATTRVERIFYFALG_BIZ_BRAND:8, MM_USERATTRVERIFYFALG_BIZ_VERIFIED:16, StatusNotifyCode_READED:1, StatusNotifyCode_ENTER_SESSION:2, StatusNotifyCode_INITED:3, StatusNotifyCode_SYNC_CONV:4, StatusNotifyCode_QUIT_SESSION:5, MM_WEBWXFUNCTION_TONE_NOT_OPEN:1, MM_WEBWXFUNCTION_NOTIFY_OPEN:2,
        MM_VERIFYUSER_ADDCONTACT:1, MM_VERIFYUSER_SENDREQUEST:2, MM_VERIFYUSER_VERIFYOK:3, MM_VERIFYUSER_VERIFYREJECT:4, MM_VERIFYUSER_SENDERREPLY:5, MM_VERIFYUSER_RECVERREPLY:6, MM_ADDSCENE_PF_QQ:4, MM_ADDSCENE_PF_EMAIL:5, MM_ADDSCENE_PF_CONTACT:6, MM_ADDSCENE_PF_WEIXIN:7, MM_ADDSCENE_PF_GROUP:8, MM_ADDSCENE_PF_UNKNOWN:9, MM_ADDSCENE_PF_MOBILE:10, EN_INFORMAT_NULL:0, EN_INFORMAT_AMR:1, EN_INFORMAT_MP3:2, EN_INFORMAT_MP4:3, EN_INFORMAT_WMA:4, EN_INFORMAT_WAV:5, EN_INFORMAT_WMV:6, EN_INFORMAT_ASF:7, EN_INFORMAT_RM:8,
        EN_INFORMAT_RMVB:9, EN_INFORMAT_AVI:10, EN_INFORMAT_MPG:11, EN_INFORMAT_MPEG:12, EN_INFORMAT_BUTT:13, MM_STATUS_VERIFY_USER:32, MMWEBWX_OPLOG_BLACKCONTACT:1, MMWEBWX_OPLOG_MODREMARKNAME:2, MMWEBWX_OPLOG_BLACKCONTACT_DELETE:0, MMWEBWX_OPLOG_BLACKCONTACT_ADD:1, MM_CHATROOM_NOTIFY_OPEN:1, MM_CHATROOM_NOTIFY_CLOSE:0, MM_MEMBER_OK:0, MM_MEMBER_NOUSER:1, MM_MEMBER_USERNAMEINVALID:2, MM_MEMBER_BLACKLIST:3, MM_MEMBER_NEEDVERIFYUSER:4, MM_MEMBER_UNSUPPORT_TALK:5})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = [];
    d.logic("init", {init:function(c) {
        var e = this;
        e.isIniting || (e.isIniting = !0, a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxinit", d.model("account").getBaseRequest(), {onsuccess:function(b) {
            d.model("contact").addContacts(b.ContactList, !0);
            var e = d.model("account");
            e.setUserInfo(b.User);
            e.setSid(a.getCookie("wxsid"));
            e.setClientVer(b.ClientVersion);
            e.setSyncKey(b.SyncKey);
            e.setHistoryConversation(b.ChatSet);
            for(var e = d.model("message"), g = b.ContactList.length - 1;0 <= g;g--) {
                e.initMessageQueue(b.ContactList[g].UserName, b.ContactList.length - g)
            }
            f = b.ContactList;
            _bIsInitOk = !0;
            c && c(d.ErrOk, b);
            d.logic("sync").notifyMobile(d.model("account").getUserName(), 3)
        }, onerror:function() {
            c && c(-1)
        }, oncomplete:function() {
            d.triggerEvent("inited");
            e.isIniting = !1
        }}))
    }, getInitedContacts:function() {
        return f
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = 0, e = 0;
    d.logic("sync", {sync:function() {
        var f = this;
        if(b.isStatusValid()) {
            if(f.isSyncing) {
                6E4 < a.now() - c && Log.e("JS Function: syncLogic sync. Do Sync Blocked, less 1 min between 2 sync!!!")
            }else {
                c = a.now();
                f.isSyncing = !0;
                var g = d.model("account"), i = g.getUserInfo();
                _sSid = g.getSid();
                _oSyncKey = g.getSyncKey();
                _sUrl = "/cgi-bin/mmwebwx-bin/webwxsync?sid=" + encodeURIComponent(_sSid);
                baseRequest = {Uin:i.Uin, Sid:_sSid};
                var j = {BaseRequest:baseRequest, SyncKey:_oSyncKey};
                a.netQueue().send(_sUrl, j, {onbefore:function() {
                    Log.d("doSync, synckey=" + JSON.stringify(j));
                    b.startMonitor()
                }, onsuccess:function(b) {
                    Log.d("doSyncSuccess");
                    f.isSyncing = !1;
                    if(null != b) {
                        var c = a.safe(function() {
                            b.SyncKey && (g.setSyncKey(b.SyncKey), g.setSkey(b.SKey), Log.d(b.SyncKey));
                            var a = b.AddMsgList;
                            if(a) {
                                var c = d.model("message"), e = d.logic("msgProcessor");
                                Log.d("addMsg, count=" + a.length);
                                for(var f = 0, h = a.length;f < h;f++) {
                                    var i = a[f];
                                    e.process(i) || c.addMessages([i])
                                }
                            }
                            if(a = b.ModContactList) {
                                c = d.model("contact");
                                for(e = 0;e < a.legnth;++e) {
                                    if(f = a[e], 0 == f.HeadImgUpdateFlag && (h = c.getContact(f.UserName)) && h.HeadImgUrl) {
                                        f.HeadImgUrl = h.HeadImgUrl
                                    }
                                }
                                e = 0;
                                for(h = a.length;e < h;e++) {
                                    f = a[e], d.util.isRoomContact(f.UserName) && (i = c.getContact(f.UserName), (!i || !i.UserName) && f.ChatRoomOwner == d.model("account").getUserName() && d.model("message").initMessageQueue(f.UserName))
                                }
                                e = 0;
                                for(h = a.length;e < h;e++) {
                                    c.addContact(a[0])
                                }
                            }
                            if(a = b.DelContactList) {
                                c = d.model("contact");
                                e = 0;
                                for(f = a.length;e < f;e++) {
                                    c.deleteContact(a[e].UserName)
                                }
                            }
                            if(a = b.Profile) {
                                c = a.BitFlag, e = d.model("account").getUserInfo(), f = !1, c & 1 && (e.UserName = a.UserName.Buff, f = !0), c & 1 && (e.NickName = a.NickName.Buff, f = !0), 1 == a.HeadImgUpdateFlag && (e.HeadImgUrl = a.HeadImgUrl, f = !0), f && d.model("account").setUserInfo(e)
                            }
                        });
                        if(0 == c && 0 != b.ContinueFlag) {
                            setTimeout(function() {
                                f.sync()
                            }, 10);
                            return
                        }
                        if(0 > c) {
                            setTimeout(function() {
                                f.syncCheck()
                            }, 10);
                            return
                        }
                    }
                    setTimeout(function() {
                        f.syncCheck()
                    }, 10);
                    e = 0
                }, onerror:function(a, b) {
                    Log.e("Cgi:" + _sUrl + ", JS Function: syncLogic sync. DoSyncError, status = " + a + ", statusCode = " + b);
                    f.isSyncing = !1;
                    setTimeout(function() {
                        f.syncCheck()
                    }, 1E3 * ((e += 5) % 30))
                }, oncomplete:function() {
                    f.isSyncing = !1;
                    b.stopMonitor()
                }})
            }
        }
    }, syncCheck:function() {
        var c = this;
        if(b.isStatusValid()) {
            var e = 1E4 - (a.now() - (c.syncCheck._lastSyncTime || 0));
            0 > e && (e = 0);
            1E4 < e && (e = 1E3);
            setTimeout(function() {
                c.syncCheck._lastSyncTime = a.now();
                for(var e = d.model("account"), g = e.getSid(), l = e.getUin(), e = e.getSyncKey().List, k = [], m = 0, n = e.length;m < n;m++) {
                    k.push(e[m].Key + "_" + e[m].Val)
                }
                b.startMonitor();
                a.ajax({url:d.getRes("url_push") + "/cgi-bin/mmwebwx-bin/synccheck", dataType:"jsonp", data:{sid:g, uin:l, deviceid:d.getDeviceId(), synckey:k.join("|")}, timeout:35E3, complete:function(a, e) {
                    debug("syncCheck onComplete.");
                    b.stopMonitor();
                    try {
                        if(f.synccheck && "0" == f.synccheck.retcode) {
                            var g = f.synccheck;
                            Log.d("syncCheckSuccess, synckey=" + k);
                            Log.d(g);
                            c.syncCheck._lastSyncTime = 0;
                            g && "0" == g.retcode && "0" != g.selector ? (c.mnSyncCheckErrCount = 0, c.sync()) : g && "0" == g.retcode ? (c.mnSyncCheckErrCount = 0, c.syncCheck()) : 3 > c.mnSyncCheckErrCount ? (c.mnSyncCheckErrCount = (c.mnSyncCheckErrCount || 0) + 1, c.sync()) : c.syncCheck()
                        }else {
                            if(!f.synccheck || !d.timeoutDetect(f.synccheck.retcode)) {
                                Log.e("syncCheckError, synckey=" + k + ", errCount=" + c.mnSyncCheckErrCount + ", status = " + e + ", statusCode = " + a.status), d.ossLog({Type:d.Constants.MMWEBWX_CONNECT_ERR}), 3 > c.mnSyncCheckErrCount ? (c.mnSyncCheckErrCount += 1, c.sync()) : c.syncCheck()
                            }
                        }
                    }catch(i) {
                        Log.e("Cgi: /cgi-bin/mmwebwx-bin/synccheck, JS Function: synccheck, try catch error: " + +i)
                    }
                    f.synccheck = null
                }})
            }, e)
        }
    }, notifyMobile:function(b, c) {
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxstatusnotify", a.extend(d.model("account").getBaseRequest(), {Code:c, FromUserName:d.model("account").getUserName(), ToUserName:b, ClientMsgId:"" + a.now()}))
    }});
    var b = {_nTimeout:45E3, _nTimer:0, _nSyncCheckRunner:0, startMonitor:function() {
        Log.d("start syncCheck monitor.");
        this._nSyncCheckRunner++;
        1 != this._nSyncCheckRunner && (Log.e("JS Function: startMonitor. Too Many SyncCheckIns are running. count = " + this._nSyncCheckRunner), this._nSyncCheckRunner = 1);
        clearTimeout(this._nTimer);
        this._nTimer = setTimeout(function() {
            Log.e("JS Function: startMonitor. Monitor timeout");
            d.logic("sync").sync()
        }, this._nTimeout)
    }, stopMonitor:function() {
        Log.d("stop syncCheck monitor.");
        this._nSyncCheckRunner--
    }, isStatusValid:function() {
        return 1 > this._nSyncCheckRunner
    }}
})(jQuery, WebMM, this);
(function(a, d, f, c) {
    d.logic("sendMsg", {sendText:function(c, b) {
        var f;
        var g = c.Msg.Content.match(/^@!@!(.*)!@!@$/);
        null != g && (a.evalVal(g[1]), f = !0);
        f || (f = a.extend(d.model("account").getBaseRequest(), c), g = {}, f.Msg.LocalID = f.Msg.ClientMsgId = a.now(), d.model("message").addMessages([a.extend(g, f.Msg, {MsgId:a.now(), MsgType:1, Status:1, CreateTime:Math.floor(a.now() / 1E3)})]), this._postText(b, f, g))
    }, resendText:function(c, b) {
        var f = a.extend(d.model("account").getBaseRequest(), {Msg:c});
        c.ResendCount = 0;
        this._postText(b, f, c)
    }, _postText:function(e, b, f) {
        e && e.onbefore && e.onbefore();
        var g = this, i = d.model("account").getSid(), j = "/cgi-bin/mmwebwx-bin/webwxsendmsg?sid=" + encodeURIComponent(i);
        b.Msg.Content = d.widget.afterEncodeEmoji(d.widget.preFilterEmoji(b.Msg.Content));
        a.netQueue("sendMsg").send(j, b, {onsuccess:function(a) {
            f.update({MsgId:a.MsgID, Status:2})
        }, onerror:function(a, d) {
            f.ResendCount == c && (f.ResendCount = 0);
            Log.e("Cgi: " + j + ", JS Function: sendmsg _postText. Send Msg Error, Ret = " + a + ", ResendCount = " + f.ResendCount + ", StatusCode = " + d);
            var i = parseInt(f.ResendCount);
            1 > i && "timeout" == a ? (f.ResendCount = i + 1, setTimeout(function() {
                g._postText(e, b, f)
            }, 1E3)) : (f.update({Status:5}), e && e.onerror && e.onerror(a))
        }})
    }, sendImg:function(c, b) {
        d.model("message").addMessages([a.extend({Status:1, MsgId:c.LocalID, MsgType:3, CreateTime:Math.floor(a.now() / 1E3)}, c)]);
        f["" + c.LocalID] = function(a, f) {
            var i = d.model("message").getMsgByLocalId(c.ToUserName, c.LocalID);
            i.FileUrl ? (-1 != f ? (i.Status = 2, i.MsgId = f) : i.Status = 5, d.triggerEvent("messageUpdated", i), b && b()) : d.widget.preLoadImg("/cgi-bin/mmwebwx-bin/webwxgetmsgimg?type=slave&MsgID=" + f, function() {
                var a = d.model("message").getMsgByLocalId(c.ToUserName, c.LocalID);
                -1 != f ? (a.Status = 2, a.MsgId = f, d.widget.preLoadImg("/cgi-bin/mmwebwx-bin/webwxgetmsgimg?MsgID=" + f)) : a.Status = 5;
                d.triggerEvent("messageUpdated", a);
                b && b()
            })
        }
    }, sendAudio:function(c, b, f) {
        c = {Status:1, LocalID:f, MsgId:f, MsgType:34, FromUserName:d.model("account").getUserName(), ToUserName:c, VoiceLength:b, CreateTime:Math.floor(a.now() / 1E3)};
        d.model("message").addMessages(c)
    }, finishSentAudio:function(a, b, c) {
        a = d.model("message").getMsgByLocalId(a, b);
        c ? (a.Status = 2, a.MsgId = c) : a.Status = 5;
        d.triggerEvent("messageUpdated", a)
    }, sendAppMsg:function(c, b) {
        var f = a.extend(d.model("account").getBaseRequest(), c);
        a.netQueue("sendMsg").send("/cgi-bin/mmwebwx-bin/webwxsendappmsg", f, {onbefore:function() {
            b && b.onbefore && b.onbefore()
        }, onsuccess:function(a) {
            var b = d.model("message").getMsgByLocalId(c.Msg.ToUserName, c.Msg.LocalID);
            b.MsgId = a.MsgID;
            b.Status = 2;
            d.triggerEvent("messageUpdated", b)
        }, onerror:function(a) {
            var f = d.model("message").getMsgByLocalId(c.Msg.ToUserName, c.Msg.LocalID);
            f.Status = 5;
            b && b.onerror && b.onerror(a);
            d.triggerEvent("messageUpdated", f)
        }, oncomplete:function() {
        }})
    }, changeSendingMsgStatus:function(a, b, c, f) {
        if(a = d.model("message").getMsgByLocalId(a, b)) {
            a.Status = c ? 2 : 5, c && (a.MsgId = f), d.triggerEvent("messageUpdated", a)
        }
    }, sendEmoji:function(c, b) {
        d.model("message").addMessages([a.extend({Status:1, MsgId:c.LocalID, MsgType:d.Constants.MM_DATA_EMOJI, CreateTime:Math.floor(a.now() / 1E3)}, c)]);
        f["" + c.LocalID] = function(a, f) {
            d.widget.preLoadImg("/cgi-bin/mmwebwx-bin/webwxgetmsgimg?type=slave&MsgID=" + f, function() {
                var a = d.model("message").getMsgByLocalId(c.ToUserName, c.LocalID);
                -1 != f ? (a.Status = 2, a.MsgId = f, d.widget.preLoadImg("/cgi-bin/mmwebwx-bin/webwxgetmsgimg?MsgID=" + f)) : a.Status = 5;
                d.triggerEvent("messageUpdated", a);
                b && b()
            })
        }
    }, sendSysCustomEmoji:function(c, b) {
        var f = a.now(), f = {LocalID:f, ClientMsgId:f, FromUserName:d.model("account").getUserName(), ToUserName:c, Content:d.widget.getTuzkiPathByMd5(b) || "", NewContent:d.widget.getTuzkiPathByMd5(b) || "", EmojiFlag:2, Type:d.Constants.MM_DATA_EMOJI, EMoticonMd5:b}, g = a.extend({Msg:f}, d.model("account").getBaseRequest()), i;
        d.model("message").addMessages([i = a.extend({Status:1, MsgId:f.LocalID, MsgType:d.Constants.MM_DATA_EMOJI, CreateTime:Math.floor(a.now() / 1E3)}, f)]);
        a.netQueue("sendEmojiMsg").send("/cgi-bin/mmwebwx-bin/webwxsendemoticon?fun=sys", g, {onbefore:function() {
        }, onsuccess:function(a) {
            i.MsgId = a.MsgID;
            i.Status = 2
        }, onerror:function() {
            i.Status = 5
        }, oncomplete:function() {
            d.triggerEvent("messageUpdated", i)
        }})
    }, sendCustomGif:function(c, b) {
        var f = b.LocalId, g = {LocalID:f, MediaId:b.MediaId, ClientMsgId:f, FromUserName:d.model("account").getUserName(), ToUserName:c, EmojiFlag:2, Type:d.Constants.MM_DATA_EMOJI}, g = a.extend({Msg:g}, d.model("account").getBaseRequest()), i = d.model("message").getMsgByLocalId(c, f);
        i.MsgType = d.Constants.MM_DATA_EMOJI;
        i.CustomGif = !0;
        a.netQueue("sendEmojiMsg").send("/cgi-bin/mmwebwx-bin/webwxsendemoticon?fun=sys", g, {onsuccess:function(a) {
            i.Status = 2;
            i.MsgId = a.MsgID;
            i.NewContent = "/cgi-bin/mmwebwx-bin/webwxgetmsgimg?type=big&MsgID=" + a.MsgID
        }, onerror:function(a) {
            Log.e("Cgi: sendemotionicon, JS funciton: sendCustomGif, Ret: " + a);
            i.Status = 5;
            i.NewContent = "/cgi-bin/mmwebwx-bin/webwxgetmsgimg?type=slave&MsgID=" + i.LocalID
        }, oncomplete:function() {
            d.triggerEvent("messageUpdated", i)
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("batchgetcontact", {batchgetContact:function(f, c) {
        var e = this, f = f || [];
        e._oContactsToGet || (e._oContactsToGet = []);
        e._oContactsGetting || (e._oContactsGetting = []);
        for(var b = 0, h = f.length;b < h;b++) {
            f[b] && f[b].UserName && (e.isContactDownloaded(f[b].UserName) || 0 <= e._fFindContactInDownloadQueue(f[b].UserName) || 0 <= e._fFindContactInDownloadingQueue(f[b].UserName) || e._oContactsToGet.push(f[b]))
        }
        0 != e._oContactsToGet.length && !e.isBatchGetting && (e.isBatchGetting = !0, b = a.extend(d.model("account").getBaseRequest(), {Count:e._oContactsToGet.length, List:e._oContactsToGet}), e._oContactsGetting = e._oContactsToGet, e._oContactsToGet = [], a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxbatchgetcontact?type=ex", b, {onsuccess:function(b) {
            var f = false;
            if(b != null && b.ContactList) {
                for(var f = d.model("contact"), h = 0, l = b.ContactList.length;h < l;h++) {
                    var k = b.ContactList[h];
                    e._oContactsGetting.splice(e._fFindContactInDownloadingQueue(k.UserName), 1);
                    f.addContact(k)
                }
                f = true
            }
            f ? c && c(true, b) : c && c(false);
            b = a.clone(e._oContactsGetting);
            e._oContactsGetting = [];
            e.isBatchGetting = false;
            b.length > 0 && e.batchgetContact(b)
        }, onerror:function() {
            c && c(false);
            var b = a.clone(e._oContactsGetting);
            e._oContactsGetting = [];
            e.isBatchGetting = false;
            b.length > 0 && e.batchgetContact(b)
        }}))
    }, isContactDownloaded:function(a) {
        var c = d.model("contact").getContact(a);
        return a == d.model("account").getUserInfo().UserName ? !0 : !(!c || !c.UserName || d.util.isRoomContact(c.UserName) && !(c.MemberList && 0 < c.MemberList.length))
    }, _fFindContactInDownloadingQueue:function(a) {
        for(var c = 0;c < this._oContactsGetting.length;++c) {
            if(this._oContactsGetting[c].UserName == a) {
                return c
            }
        }
        return-1
    }, _fFindContactInDownloadQueue:function(a) {
        for(var c = 0;c < this._oContactsToGet.length;++c) {
            if(this._oContactsToGet[c].UserName == a) {
                return c
            }
        }
        return-1
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    function f(a, b) {
        if(c) {
            if(a.isRoom && !b.isRoom) {
                return 1
            }
            if(!a.isRoom && b.isRoom) {
                return-1
            }
        }
        if(a.weight && !b.weight) {
            return-1
        }
        if(!a.weight && b.weight) {
            return 1
        }
        if(a.weight && b.weight) {
            return b.weight - a.weight
        }
        if(a.msgCreateTime && !b.msgCreateTime) {
            return-1
        }
        if(b.msgCreateTime && !a.msgCreateTime) {
            return 1
        }
        if(a.msgCreateTime && b.msgCreateTime) {
            var d = b.msgCreateTime - a.msgCreateTime;
            if(0 != d) {
                return d
            }
        }
        return a.name.localeCompare(b.name)
    }
    var c = "", e = d.model("message"), b = d.model("contact");
    d.model("account");
    d.logic("getconversation", {get:function(a) {
        var d = [], i = a ? b.getAllCanChatContactUserName(a) : e.getQueueUserNames();
        c = a = a || "";
        for(var j = 0, l = i.length;j < l;j++) {
            var k = this.genConversation(i[j]), m = k.digest || "";
            (!k.contact || !k.contact.canSearch(a, !0)) && -1 == m.search(a) || d.push(k)
        }
        d.sort(f);
        if(c) {
            j = i = a = 0;
            for(l = d.length;j < l;j++) {
                d[j].isRoom ? i++ : a++
            }
            if(5 < a) {
                for(j = d.length - 1;0 <= j && (d[j].isRoom || !(0.8 > d[j].weight) || !(d.splice(j, 1), 5 >= --a));j--) {
                }
            }
            if(5 < i) {
                for(j = d.length - 1;0 <= j && (!(d[j].isRoom && 0.8 > d[j].weight) || !(d.splice(j, 1), 5 >= --i));j--) {
                }
            }
        }
        return d
    }, genConversation:function(a) {
        var f = b.getContact(a), i = e.getLastMessage(a), j = f && f.DisplayName || i.actualSender || "", l = "", k = !1, m = "", n = "", q = e.getUnreadMsgsCount(a), p = f ? f.initOrder : 0;
        d.util.isRoomContact(a) && (k = !0);
        l = d.util.getNormalAvatarUrl(a);
        i.CreateTime && (m = -9999 == i.MsgType ? "" : d.util.formatConversationListTime(new Date(1E3 * i.CreateTime)));
        i.MsgType && (n = d.util.genMessageDigest(i));
        return{avatar:l, userName:a, name:j, time:m, unread:q, invisible:!1, type:i.MsgType, status:i.Status, digest:n, isRoom:k, memCount:k && f && f.MemberCount, initOrder:p, msgCreateTime:i.CreateTime, weight:c && f && f.weight || i.weight, muted:f && f.isMuted() || !1, contact:f}
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = !1;
    d.logic("contact", {getAllContacts:function() {
        f || a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxgetcontact", {}, {onsuccess:function(a) {
            if(a) {
                for(var e = 0, b = a.MemberList.length;e < b;e++) {
                    a.MemberList[e].isContact = !0
                }
                d.model("contact").addContacts(a.MemberList);
                f = !0
            }
        }})
    }, hasGotAllContacts:function() {
        return!!f
    }, getAllSortedGroups:function() {
        for(var a = d.model("contact").getAllChatroomContact() || [], e = 0, b = a.length;e < b;e++) {
            var f = d.model("message").getLastMessage(a[e].UserName);
            a[e].lastUpdateTime = f && f.CreateTime || -1
        }
        return a = a.sort(function(a, b) {
            return b.lastUpdateTime - a.lastUpdateTime
        })
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("createChatRoom", {create:function(f, c, e) {
        if(c && c.length) {
            for(var b = [], h = d.model("contact"), g = d.model("account").getBaseRequest(), i = 0, j = c.length;i < j;i++) {
                var l = h.getContact(c[i]);
                b.push({Uin:l.Uin, UserName:l.UserName, NickName:l.NickName})
            }
            g = a.extend(g, {Topic:f, MemberCount:b.length, MemberList:b});
            a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxcreatechatroom", g, {onbefore:function() {
                e.onbefore && e.onbefore()
            }, onsuccess:function(a) {
                if(a) {
                    var b = a.ChatRoomName, c = d.model("message").getMessages(b);
                    d.model("contact").addContact({UserName:a.ChatRoomName, RemarkName:"", NickName:"", MemberCount:a.MemberCount + 1, MemberList:a.MemberList.push(d.model("contact").getContact(d.model("account").getUserName()) || d.model("account").getUserInfo())});
                    c.length || d.model("message").initMessageQueue(b)
                }
                e.onsuccess && e.onsuccess(a)
            }, onerror:function() {
                e.onerror && e.onerror()
            }})
        }
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = d.model("photoalbum");
    d.logic("photoalbum", {getPhotoAlbumByUserName:function(a) {
        return(a = f.getByUserName(a)) ? a : null
    }, requestPhotoAlbumByUserName:function(c, d) {
        var b = this, h = WebMM.model("photoalbum").getCurrentIdByUserName(c), g = a.extend(WebMM.model("account").getBaseRequest(), {FirstPageMd5:"", UserName:c, MaxId:h, Source:0, MinFilterId:0, LastRequestTime:0, PicCount:0});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxsnsuserpage", g, {onsuccess:function(a) {
            a = b._photoAlbumDataHandle(a);
            if(!a) {
                return d.onerror && d.onerror(c), !1
            }
            0 < h ? f.addByUserName(c, a) : f.setByUserName(c, a);
            d.onsuccess(c, a)
        }, onerror:function(a, b) {
            Log.d(a, b);
            d.onerror && d.onerror(c)
        }})
    }, _photoAlbumDataHandle:function(c) {
        var e = c.ObjectList;
        if(!e) {
            return Log.e("Cannot Get Photo Album ObjectList"), !1
        }
        for(var b = 0, f = e.length;b < f;++b) {
            for(var g = e[b].CommentUserList, i = d.widget.filterQQFace, j = 0, l = g.length;j < l;++j) {
                g[j].Content = i(g[j].Content), g[j].Content = g[j].Content.replace(/&lt;span class=&quot;(emoji emoji.*?)&quot;&gt;&lt;\/span&gt;/g, "<span class='$1'></span>")
            }
            g = a.xml2json(a.htmlDecode(e[b].ObjectDesc));
            g.contentDesc = i(g.contentDesc.replace(/\[span class="(emoji emoji.*?)"\]\[\/span\]/g, "<span class='$1'></span>"));
            i = g.ContentObject.mediaList.media;
            jQuery.isArray(i) || (j = [], j.push(i), g.ContentObject.mediaList.media = j);
            e[b].ObjectDesc = g
        }
        return c
    }, _requestPhotoAlbumByNum:function(c, d, b) {
        var f = this, b = a.extend(WebMM.model("account").getBaseRequest(), {FirstPageMd5:"", UserName:c, MaxId:0, Source:0, MinFilterId:0, LastRequestTime:0, PicCount:b || 0});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxsnsuserpage", b, {onsuccess:function(a) {
            a = f._photoAlbumDataHandle(a);
            if(!a) {
                return d.onerror && d.onerror(c), !1
            }
            d.onsuccess(c, a)
        }, onerror:function(a, b) {
            Log.d(a, b);
            d.onerror && d.onerror(c)
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("modChatroom", {addMember:function(a, c, d) {
        this._update("addmember", a, c, "", "", d)
    }, delMember:function(a, c) {
        this._update("delmember", a, "", c, "");
        for(var e = d.model("contact").getContact(a), b = e && e.MemberList || [], h = 0, g = b.length;h < g;h++) {
            if(b[h].UserName == c) {
                b.splice(h, 1);
                e.MemberCount = b.length;
                d.model("contact").addContact(e);
                break
            }
        }
    }, modTopic:function(a, c) {
        this._update("modtopic", a, "", "", c)
    }, _update:function(f, c, e, b, h, g) {
        e = a.extend({AddMemberList:e, DelMemberList:b, NewTopic:h, ChatRoomName:c}, d.model("account").getBaseRequest());
        a.netQueue("modChatroom").send("/cgi-bin/mmwebwx-bin/webwxupdatechatroom?fun=" + f, e, {onsuccess:function(a) {
            if("delmember" == f) {
                for(var e = d.model("contact").getContact(c), h = e.MemberList.length - 1;0 <= h;h--) {
                    e.MemberList[h].UserName == b && e.MemberList.splice(h, 1)
                }
                e.MemberCount = e.MemberList.length;
                d.model("contact").addContact(e)
            }
            g && g.onsuccess && g.onsuccess(a)
        }, onerror:function() {
        }})
    }, quit:function(f) {
        f = a.extend({AddMemberList:"", DelMemberList:"", NewTopic:"", ChatRoomName:f}, d.model("account").getBaseRequest());
        a.netQueue("modChatroom").send("/cgi-bin/mmwebwx-bin/webwxupdatechatroom?fun=quitchatroom", f, {onsuccess:function() {
        }, onerror:function() {
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = 0;
    d.logic("loadHistoryMsg", {loadMore:function(c, e) {
        var b = a.extend({ChatUserName:c, StartMsgId:f, Count:10}, d.model("account").getBaseRequest()), h = d.model("message").getFirstMessage(c);
        a.netQueue("loadHistoryMsg").send("/cgi-bin/mmwebwx-bin/webwxgetmsg", b, {onbefore:function() {
            h.Status = d.Constants.STATE_SENDING
        }, onsuccess:function(a) {
            var b = a.AddMsgList.length;
            0 >= b || (f = a.AddMsgList[b - 1].MsgId, d.model("message").addMessages(a.AddMsgList, 1), h.Status = d.Constants.STATE_SENT, h.ContinueFlag = a.ContinueFlag)
        }, onerror:function() {
            h.Status = d.Constants.STATE_FAILED
        }, oncomplete:function() {
            e && e()
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("msgProcessor", {process:function(f) {
        if(f.MsgType == d.Constants.MM_DATA_STATUSNOTIFY) {
            return this._statusNotifyProcessor(f), !0
        }
        if(f.MsgType == d.Constants.MM_DATA_SYSNOTICE) {
            return a.evalVal(f.Content), !0
        }
        f.MsgType == d.Constants.MM_DATA_APPMSG ? this._brandMsgProcess(f) : f.MsgType == d.Constants.MM_DATA_APPMSG ? this._appMsgProcess(f) : f.MsgType == d.Constants.MM_DATA_EMOJI ? this._emojiMsgProcess(f) : "newsapp" == f.FromUserName && f.MsgType == d.Constants.MM_DATA_TEXT ? this._newsMsgProcess(f) : d.util.isRecommendAssistant(f.MsgType) ? this._recommendMsgProcess(f) : f.MsgType == d.Constants.MM_DATA_SHARECARD ? this._shareCardProcess(f) : f.MsgType == d.Constants.MM_DATA_SYS && this._systemMsgProcess(f);
        return!1
    }, _statusNotifyProcessor:function(f) {
        var c = d.model("message");
        if(f.StatusNotifyCode == d.Constants.StatusNotifyCode_ENTER_SESSION) {
            c.initMessageQueue(f.ToUserName), d.triggerEvent("focusToTop", f.ToUserName)
        }else {
            if(f.StatusNotifyCode == d.Constants.StatusNotifyCode_SYNC_CONV) {
                for(var e = a.trim(f.StatusNotifyUserName).split(","), b = 0, c = e.length;b < c;b++) {
                    d.util.isSpUser(e[b]) || function() {
                        var a = e[b], c = b;
                        setTimeout(function() {
                            d.model("message").initMessageQueue(a, -c)
                        })
                    }()
                }
                for(var h = d.logic("init").getInitedContacts(), b = 0, c = h.length;b < c;b++) {
                    var g = h[b].UserName, i = !1;
                    if(!d.util.isFileHelper(g)) {
                        for(var j = 0, l = e.length;j < l;j++) {
                            g == e[j] && (i = !0)
                        }
                        i || d.model("message").deleteMessage(g)
                    }
                }
            }
        }
        (f.StatusNotifyCode == d.Constants.StatusNotifyCode_ENTER_SESSION || f.StatusNotifyCode == d.Constants.StatusNotifyCode_QUIT_SESSION) && d.model("message").markMsgsRead(f.ToUserName) && d.triggerEvent("markMsgRead", f.ToUserName)
    }, _appMsgProcess:function(a) {
        a.AppMsgType != d.Constants.APPMSGTYPE_ATTACH && (a.MsgType = d.Constants.MM_DATA_APPMSG_UNSUPPORT)
    }, _emojiMsgProcess:function(a) {
        a.NewContent = d.widget.parseTuzki(a.Content);
        a.NewContent || (a.NewContent = "/cgi-bin/mmwebwx-bin/webwxgetmsgimg?type=big&MsgID=" + a.MsgId)
    }, _newsMsgProcess:function(f) {
        f.MsgType = d.Constants.MM_DATA_READER_TYPE;
        f.Object = a.xml2json(a.htmlDecode(f.Content).replace(/<br\/>/ig, ""));
        var c = f.Object.category.item = f.Object.category.newitem;
        if(1 == f.Object.category.count) {
            c.url = c.url.replace("refer=nwx", "refer=webwx");
            c.title = a.htmlEncode(c.title);
            c.digest = a.htmlEncode(c.digest);
            var e = c.cover.split("|");
            3 == e.length && (c.cover = e[0], c.width = e[1], c.height = e[2])
        }else {
            for(var b = 0, h = c.length;b < h;b++) {
                c[b].url = c[b].url.replace("refer=nwx", "refer=webwx"), c[b].title = a.htmlEncode(c[b].title), e = c[b].cover.split("|"), 3 == e.length && (c[b].cover = e[0], c[b].width = e[1], c[b].height = e[2])
            }
        }
        debug(function() {
            console.info(f.Object)
        });
        f.Content = c.title || c[0] && c[0].title
    }, _brandMsgProcess:function(f) {
        var c = a.htmlDecode(f.Content).replace(/<br\/>/ig, "");
        if(d.util.isRoomContact(f.FromUserName)) {
            var e = c.indexOf(":");
            f.Content = c.substr(0, e + 1) + "<br/>";
            c = c.substr(e + 1)
        }else {
            f.Content = ""
        }
        f.Object = a.xml2json(c);
        debug(function() {
            console.info(f.Object)
        });
        if(f.Object.appmsg.mmreader) {
            f.MsgType = d.Constants.MM_DATA_READER_TYPE;
            f.Object = f.Object.appmsg.mmreader;
            c = f.Object.category.item;
            if(1 == f.Object.category.count) {
                c.title = a.htmlEncode(c.title), c.digest = a.htmlEncode(c.digest), e = c.cover.split("|"), 3 == e.length && (c.cover = e[0], c.width = e[1], c.height = e[2])
            }else {
                for(var b = 0, h = c.length;b < h;b++) {
                    c[b].title = a.htmlEncode(c[b].title), e = c[b].cover.split("|"), 3 == e.length && (c[b].cover = e[0], c[b].width = e[1], c[b].height = e[2])
                }
            }
            f.Content += c.title || c[0] && c[0].title
        }else {
            f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_TEXT ? (f.MsgType = d.Constants.MM_DATA_APP_MSG_TEXT_TYPE, f.Content += f.Object.appmsg.title = a.htmlEncode(f.Object.appmsg.title)) : f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_IMG ? f.MsgType = d.Constants.MM_DATA_APP_MSG_IMG_TYPE : f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_AUDIO ? (f.MsgType = d.Constants.MM_DATA_APP_MSG_AUDIO_TYPE, f.Object.appmsg.title = a.htmlEncode(f.Object.appmsg.title),
                f.Object.appmsg.des = a.htmlEncode(f.Object.appmsg.des)) : f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_VIDEO ? (f.MsgType = d.Constants.MM_DATA_APP_MSG_VIDEO_TYPE, f.Object.appmsg.title = a.htmlEncode(f.Object.appmsg.title), f.Object.appmsg.des = a.htmlEncode(f.Object.appmsg.des)) : f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_URL ? (f.MsgType = d.Constants.MM_DATA_APP_MSG_URL_TYPE, f.Object.appmsg.title = a.htmlEncode(f.Object.appmsg.title), f.Object.appmsg.des =
                a.htmlEncode(f.Object.appmsg.des)) : f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_ATTACH || (f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_OPEN ? (f.MsgType = d.Constants.MM_DATA_APP_MSG_OPEN_TYPE, f.Object.appmsg.title = a.htmlEncode(f.Object.appmsg.title), f.Object.appmsg.des = a.htmlEncode(f.Object.appmsg.des)) : f.Object.appmsg && f.Object.appmsg.type == d.Constants.APPMSGTYPE_EMOJI && (f.MsgType = d.Constants.MM_DATA_APP_MSG_EMOJI_TYPE, f.Object.appmsg.title =
                a.htmlEncode(f.Object.appmsg.title), f.Object.appmsg.des = a.htmlEncode(f.Object.appmsg.des)))
        }
    }, _recommendMsgProcess:function(f) {
        f.Contact = f.RecommendInfo;
        f.Content = f.MsgType == d.Constants.MM_DATA_VERIFYMSG ? a.tmpl(d.getRes("verify_msg_digest"), {name:f.Contact.NickName || f.Contact.UserName}) : a.tmpl(d.getRes("text_posible_friend_msg_digest"), {name:f.Contact.NickName || f.Contact.UserName});
        debug(function() {
            console.info(f)
        })
    }, _shareCardProcess:function(f) {
        f.Contact = f.RecommendInfo;
        var c;
        d.util.isRoomContact(f.FromUserName) ? (c = d.util.getRoomMsgActualSender(f), f.Content = c + ":<br/>") : (c = f.FromUserName, f.Content = "");
        c == d.model("account").getUserName() ? (c = (c = d.model("contact").getContact(f.ToUserName)) && (c.RemarkName || c.NickName) || f.ToUserName, f.Content += a.tmpl(d.getRes("sharecard_msg_digest_to"), {NickName:f.Contact.NickName || f.Contact.UserName, ToNickName:c})) : f.Content += a.tmpl(d.getRes("sharecard_msg_digest_from"), {FromNickName:c, NickName:f.Contact.NickName || f.Contact.UserName});
        debug(function() {
            console.info(f)
        })
    }, _systemMsgProcess:function(d) {
        var c = d.Content.match(/&lt;a href=&quot;.*?&quot;.*?&gt;.*?&lt;\/a&gt;/g);
        if(c) {
            for(var e, b, h = 0, g = c.length;h < g;++h) {
                e = /&lt;a href=&quot;(.*?)&quot;.*?&gt;.*?&lt;\/a&gt;/.exec(c[h]);
                if(!e || !e[1]) {
                    break
                }
                b = a.htmlDecode(e[1]);
                if(/^(weixin:\/\/findfriend\/verifycontact)$/.test(b) || a.isUrl(b) && /\.qq\.com/.test(b)) {
                    d.Content = d.Content.replace(e[0], a.htmlDecode(e[0]))
                }
                d.Content = d.Content.replace(/<a href="weixin:\/\/findfriend\/verifycontact">/, '<a click="verifyContact" href="javascript:;">')
            }
        }
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("setting", {set:function(f, c) {
        var e = a.extend(d.model("account").getBaseRequest(), {FunctionId:f, Value:c});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxsetting", e, {onsuccess:function() {
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("userverify", {verify:function(f, c, e, b, h, g) {
        var i = d.model("account").getBaseRequest();
        i.Opcode = c || d.Constants.MM_VERIFYUSER_VERIFYOK;
        i.VerifyUserListSize = 1;
        i.VerifyUserList = [{Value:f, VerifyUserTicket:g || ""}];
        i.VerifyContent = e;
        i.SceneListCount = 1;
        i.SceneList = [b];
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxverifyuser", i, {onsuccess:function() {
            h && h.onsuccess && h.onsuccess()
        }, onerror:function() {
            h && h.onerror && h.onerror()
        }})
    }, verifyUniGroupList:function(f, c, e, b) {
        var h = d.model("account").getBaseRequest(), g = [], i = [];
        h.Opcode = c || d.Constants.MM_VERIFYUSER_VERIFYOK;
        h.VerifyUserListSize = h.SceneListCount = f.length;
        h.VerifyContent = e;
        c = 0;
        for(e = f.length;c < e;++c) {
            g.push({Value:f[c]}), i.push(14)
        }
        h.VerifyUserList = g;
        h.SceneList = i;
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxverifyuser", h, {onsuccess:function() {
            b && b.onsuccess && b.onsuccess()
        }, onerror:function() {
            b && b.onerror && b.onerror()
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("modifyavatar", {modify:function(f, c, e) {
        c = a.extend(d.model("account").getBaseRequest(), {MediaId:f, UserName:d.model("account").getUserName(), CropWidth:c[3], CropHeight:c[2], CropLeftTopX:c[1], CropLeftTopY:c[0], Width:c[4], Height:c[5]});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxmodifyheadimg" + (f ? "" : "?source=orghd"), c, {onsuccess:function() {
            e && e.onsuccess && e.onsuccess()
        }, onerror:function() {
            e && e.onerror && e.onerror()
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("oplog", {setRemarkName:function(f, c) {
        var e = a.extend(WebMM.model("account").getBaseRequest(), {CmdId:d.Constants.MMWEBWX_OPLOG_MODREMARKNAME, UserName:f, BlackType:0, RemarkName:c});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxoplog", e, {onsuccess:function() {
        }, onerror:function(a, c) {
            Log.e("Cgi: /cgi-bin/mmwebwx-bin/webwxoplog, JS Function: setRemarkName, RetCode: " + a + ", ErrMsg: " + c)
        }})
    }, blackContact:function(f, c) {
        var e = d.model("contact").getContact(f), e = a.extend(WebMM.model("account").getBaseRequest(), {CmdId:d.Constants.MMWEBWX_OPLOG_BLACKCONTACT, UserName:f, BlackType:c, RemarkName:e.RemarkName});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxoplog", e, {onsuccess:function() {
        }, onerror:function(a, c) {
            Log.e("Cgi: /cgi-bin/mmwebwx-bin/webwxoplog, JS Function: blackContact, RetCode: " + a + ", ErrMsg: " + c)
        }})
    }, _op:function(f, c, e) {
        f = a.extend(d.model("account").getBaseRequest(), {Opcode:f}, c);
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxoplog", f, e || {})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.logic("feedback", {send:function(d) {
        d = a.extend(WebMM.model("account").getBaseRequest(), {MachineType:"webwx", Content:d, ReportType:0});
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxsendfeedback", d, {onerror:function(a) {
            Log.e("Cgi: /cgi-bin/mmwebwx-bin/webwxsendfeedback, JS Function: feedback send, RetCode: " + a + ", Can not feedback")
        }})
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    d.model("message");
    var c = d.model("contact"), e = d.model("account");
    d.util = d.util || {};
    d.util.getProxyXHR = function(b) {
        try {
            return a("#" + b).length && a("#" + b)[0].contentWindow.window.xhr
        }catch(c) {
            return null
        }
    };
    d.util.logout = function(b) {
        f.onbeforeunload = null;
        a.form("/cgi-bin/mmwebwx-bin/webwxlogout?redirect=1&type=" + (b || 0), {sid:e.getSid(), uin:e.getUin()})
    };
    d.util.batchgetUndownloadedContactInMesssage = function(a) {
        if(a) {
            for(var c = [], e = 0, f = a.length;e < f;++e) {
                var j = a[e];
                c.push(j.FromUserName);
                c.push(j.ToUserName);
                j.actualSender && c.push(j.actualSender)
            }
            d.util.batchgetUndownloadedContact(c)
        }
    };
    d.util.batchgetUndownloadedContact = function(a) {
        for(var e = d.logic("batchgetcontact"), f = [], i = 0, j = a.length;i < j;++i) {
            var l = a[i];
            e.isContactDownloaded(l) || f.push({UserName:l, ChatRoomId:""});
            if(d.util.isRoomContact(l) && (l = c.getContact(l)) && l.MemberList) {
                for(var k = 0, j = l.MemberList.length;k < j;++k) {
                    var m = l.MemberList[k].UserName;
                    e.isContactDownloaded(m) || f.push({UserName:m, ChatRoomId:l.Uin})
                }
            }
        }
        f.length && e.batchgetContact(f)
    };
    d.util.getNormalAvatarUrl = function(a, f) {
        var g;
        g = f || "";
        if(a) {
            if(a == e.getUserName()) {
                g = (g = e.getUserInfo().HeadImgUrl) && 0 < g.length ? g : d.getRes("img_def_avatar")
            }else {
                if(d.util.isRoomContact(a)) {
                    var i = c.getContact(a);
                    g = i && i.HeadImgUrl ? i.HeadImgUrl : "/cgi-bin/mmwebwx-bin/webwxgetheadimg?type=slave&username=" + encodeURIComponent(a) + "&count=" + (i && i.MemberCount)
                }else {
                    (i = c.getContact(a)) && i.HeadImgUrl && 0 < i.HeadImgUrl.length ? g = i.HeadImgUrl : (i = "", d.util.isRoomContact(g) && (i += "&chatroomid=" + g.split("@")[0]), g = "/cgi-bin/mmwebwx-bin/webwxgeticon?username=" + a + i)
                }
            }
            g = g || ""
        }else {
            g = ""
        }
        return g
    };
    _fFormatTimeInDay = function(b, c) {
        var e = b.getTime() / 1E3 - c.getTime() / 1E3;
        if(60 > e) {
            return d.getRes("text_in_one_minute")
        }
        if(3600 > e) {
            return Math.floor(e / 60) + d.getRes("text_in_minutes")
        }
        var e = c.getHours(), f = "", f = 6 > e ? d.getRes("text_dawn") : 12 > e ? d.getRes("text_morning") : 13 > e ? d.getRes("text_noon") : 18 > e ? d.getRes("text_afternoon") : d.getRes("text_evening");
        12 < e && (e -= 12);
        return f + e + ":" + a.formatNum(c.getMinutes(), 2)
    };
    _fFormatDayAndYear = function(a, c) {
        if(a.getFullYear() != c.getFullYear()) {
            return c.getFullYear() + d.getRes("text_year") + (c.getMonth() + 1) + d.getRes("text_month") + c.getDate() + d.getRes("text_day")
        }
        var e = Math.floor(a.getTime() / 864E5) - Math.floor(c.getTime() / 864E5);
        if(0 == e) {
            return""
        }
        if(1 == e) {
            return d.getRes("text_yesterday")
        }
        if(7 > e) {
            e = c.getDay();
            0 == e && (e = 7);
            var f = a.getDay();
            0 == f && (f = 7);
            if(f > e) {
                return d.getRes(" text_monday text_tuesday text_wednesday text_thursday text_friday text_saturday text_sunday".split(" ")[e])
            }
        }
        return c.getMonth() + 1 + d.getRes("text_month") + c.getDate() + d.getRes("text_day")
    };
    d.util.formatChatMsgListTime = function(a) {
        var c = new Date;
        return _fFormatDayAndYear(c, a) + _fFormatTimeInDay(c, a)
    };
    d.util.formatConversationListTime = function(b) {
        return b.getHours() + ":" + a.formatNum(b.getMinutes(), 2)
    };
    d.util.createNewSession = function(b) {
        d.model("message").getMessages(b);
        d.model("message").initMessageQueue(b);
        a.hash("chat?userName=" + b);
        d.triggerEvent("switchToChatPanel");
        d.triggerEvent("focusToTop", b)
    };
    d.util.getChatTitle = function(b) {
        if(!b) {
            return""
        }
        b.DisplayName || (b.DisplayName = this.getContactDisplayName(b));
        return d.util.isRoomContact(b.UserName) && !b.RemarkName && !b.NickName ? a.tmpl(d.getRes("text_title_group"), b.MemberList) : d.util.isRoomContact(b.UserName) ? a.tmpl(d.getRes("text_title_group_remark"), {DisplayName:b.DisplayName, Count:b.MemberCount}) : b.DisplayName
    };
    d.util.verificationPopup = function(b, c, e, f, j) {
        var l = "string" == typeof c ? d.model("contact").getContact(c) : c;
        l && (e.confirm(a.tmpl(b), {ok:function() {
            var b = a("#verification_request"), c = a.stripStr(a.trim(b.find("input[type=text]").val()), 40);
            if(j && j.notEmpty && !c) {
                return!1
            }
            d.logic("userverify").verify(l.RecommendInfo && l.RecommendInfo.UserName || l.UserName, j && j.type || d.Constants.MM_VERIFYUSER_SENDREQUEST, c, l && l.scene || 0, {onsuccess:function() {
                e.showTips(b.attr("addSuccTips"), !0, null);
                f && f.onsuccess && f.onsuccess(c)
            }, onerror:function() {
                e.showTips(b.attr("addErrTips"), !1, null);
                f && f.onerror && f.onerror()
            }}, j && j.ticket)
        }}, "verificationRequest"), a.setInputLength(a("#verification_request").find("input"), 40))
    };
    d.util.verificationGroupPopup = function(b, c, e) {
        b && (c.confirm(a.tmpl("verification_add_group_request"), {ok:function() {
            var f = a("#verification_request"), j = a.stripStr(a.trim(f.find("input[type=text]").val()), 40);
            d.logic("userverify").verifyUniGroupList(b, d.Constants.MM_VERIFYUSER_SENDREQUEST, j, {onsuccess:function() {
                c.showTips(f.attr("addSuccTips"), !0, null);
                e && e.onsuccess && e.onsuccess(j)
            }, onerror:function() {
                c.showTips(f.attr("addErrTips"), !1, null);
                e && e.onerror && e.onerror()
            }})
        }}, "verificationRequest"), a.setInputLength(a("#verification_request").find("input"), 40))
    }
})(jQuery, WebMM, this);
(function(a, d, f) {
    d.createCtrl("root", {init:function() {
        function c() {
            var b = document.body.clientHeight;
            f.height(b - 254);
            i.height(b - 233);
            g.height(b - 134);
            j.height(f.height());
            a("#chattingmgr_list").height(b - 340)
        }
        var d = this;
        if(a("#container").isShow()) {
            d.appStart()
        }else {
            var b = setInterval(function() {
                a("#container").isShow() && (clearInterval(b), d.appStart())
            }, 100)
        }
        var f = a(".chatPanel .listContentWrap"), g = a(".chatContainer"), i = a(".chatPanel .chatScorll"), j = a("#vernierContainer");
        a(window).resize(function() {
            c()
        });
        c()
    }, active:function() {
    }, appStart:function() {
        var c = this;
        d.logic("init").init(function(e) {
            if(e == d.ErrOk) {
                d.logic("sync").sync(), d.logic("contact").getAllContacts()
            }else {
                if(-1 == e) {
                    c.alert(d.getRes("init_error_to_refresh"), {ok:function() {
                        location.reload()
                    }})
                }else {
                    if(d.timeoutDetect(e)) {
                        return
                    }
                    c.alert(d.getRes("text_init_error") + " Error Code: " + e, {ok:function() {
                        f.onbeforeunload = null;
                        d.util.logout()
                    }})
                }
            }
            f.t_t = "";
            a.getCookie("wxloadtime") && (a.setCookie("wxstaytime", a.getCookie("wxloadtime")), a.delCookie("wxloadtime"))
        });
        0 > location.href.indexOf("dev.web") && (f.onbeforeunload = function() {
            return d.getRes("text_leave_confirm")
        })
    }, enterSession:function(c, e) {
        var b = e.attr("userName") || e.attr("un"), f = d.model("contact").getContact(b);
        f && (!f.isSelf() || WebMM.model("account").isHigherVer()) && (f.isContact() || f.isRoomContact() ? d.util.createNewSession(b) : this.alert(a.tmpl(d.getRes("text_is_not_weixin_contact"), {name:f.DisplayName})))
    }, showProfile:function(c, d) {
        a.hash((a.hash() || "chat") + "/popupcontactprofile?userName=" + d.attr("userName"))
    }, showPhotoAlbum:function(c, d) {
        a.hash((a.hash() || "chat") + "/popupphotoalbum?userName=" + d.attr("userName"));
        return!1
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = "", e = !1, b = a("#chatMainPanel"), h = a("#chatDetailPanel"), g = null, i = a("#leftOpBtn"), j = a("#rightOpBtn");
    d.createCtrl("chat", {init:function() {
        this.accountUpdated()
    }, active:function(a) {
        c = a.userName;
        this._updateChatTitle();
        e && this.toggleChatMgr();
        this._refreshRightOptBtn()
    }, inactive:function() {
    }, accountUpdated:function() {
        var b = d.model("account").getUserInfo();
        b && (b.name = b.NickName && 0 < b.NickName.length ? b.NickName : b.UserName, b.avatar = d.util.getNormalAvatarUrl(b.UserName), a("#profile").html(a.tmpl("chat_profile", b)))
    }, messageAdded:function() {
    }, contactAdded:function(a) {
        a.UserName == c && (this._updateChatTitle(), this._refreshRightOptBtn())
    }, contactUpdated:function(a) {
        a.UserName == c && (this._updateChatTitle(), this._refreshRightOptBtn())
    }, getAllContacts:function() {
        d.logic("contact").getAllContacts()
    }, toggleSysMenu:function() {
        var b = this.getDom$().find(".operaterBox");
        d.globalEventSetting({globalIntercept:!b.isShow(), interceptDom$:b});
        b.html(a.tmpl("chat_operaterBoxPanel", d.model("account").getUserInfo()));
        a.browser.msie ? b.toggle() : b.fadeToggle("fast")
    }, logout:function() {
        this.confirm(d.getRes("text_logout_confirm"), {ok:function() {
            f.onbeforeunload = null;
            d.util.logout(0)
        }});
        this.toggleSysMenu()
    }, toggleNotify:function(b, c) {
        var e = !!d.model("account").isNotifyOpen() && 0 == MMNotification.checkPermission();
        2 == MMNotification.checkPermission() ? this.alert(c.attr("tip"), {ok:function() {
            a.isChrome()
        }}) : (1 == MMNotification.checkPermission() && MMNotification.requestPermission(function() {
        }), d.model("account").setNotifyOpen(!e), d.logic("setting").set(d.Constants.MM_WEBWXFUNCTION_NOTIFY_OPEN, e ? 0 : 1), a("#operaterBox").html(a.tmpl("chat_operaterBoxPanel", d.model("account").getUserInfo())), 0 != MMNotification.checkPermission() && this.toggleSysMenu())
    }, toggleMute:function() {
        var b = d.model("account").isMute();
        d.model("account").setMute(!b);
        d.logic("setting").set(d.Constants.MM_WEBWXFUNCTION_TONE_NOT_OPEN, b ? 0 : 1);
        a("#operaterBox").html(a.tmpl("chat_operaterBoxPanel", d.model("account").getUserInfo()))
    }, noHandledKeyDown:function(b) {
        a.isHotkey(b, "esc") && (b = a("#mask"), b.isShow() && b.click())
    }, noHandledClick:function() {
        this.getDom$().find(".operaterBox").isShow() && this.toggleSysMenu()
    }, _updateChatTitle:function() {
        var b = d.model("contact").getContact(c);
        null == g && (g = a("#messagePanelTitle"));
        g.html(d.util.getChatTitle(b))
    }, createChatroom:function() {
        a.hash((a.hash() || "chat") + "/createchatroom");
        this.toggleSysMenu()
    }, closeChat:function() {
        a.hash("chat")
    }, toggleChatMgr:function() {
        var a = this;
        e ? a.switchToChatPanel() : (e = !e, b.css({left:0, top:0}).show().stop().animate({left:-b.width()}), h.css({left:b.width(), top:0}).show().stop().animate({left:0}, function() {
            a.getDom$().find(".chatName").css("opacity", 1);
            a._refreshRightOptBtn();
            d.triggerEvent("setChatPanelStatus", e)
        }), a.getDom$().find(".chatName").css("opacity", 0.5))
    }, switchToChatPanel:function() {
        if(e) {
            var a = this;
            e = !e;
            b.show().stop().animate({left:0});
            h.show().stop().animate({left:b.width()}, function() {
                a.getDom$().find(".chatName").css("opacity", 1);
                a._refreshRightOptBtn();
                d.triggerEvent("setChatPanelStatus", e)
            });
            a.getDom$().find(".chatName").css("opacity", 0.5)
        }
    }, _refreshRightOptBtn:function() {
        var a = d.model("contact").getContact(c);
        a && !e ? (j[a.isBrandContact() || a.isFileHelper() || a.isRecommendHelper() || a.isNewsApp() ? "hide" : "show"](), i.hide()) : e && (j.hide(), i.show())
    }, showEditableTip:function() {
        debug("showTip")
    }, popupModifyAvatarWin:function() {
        a.hash((a.hash() || "chat") + "/modifyavatar")
    }, feedback:function() {
        a.hash((a.hash() || "chat") + "/feedback");
        this.toggleSysMenu()
    }})
})(jQuery, WebMM, this);
(function(a, d, f, c) {
    var e = !0, b = !0, h = f.onfocus = function() {
        e = !0;
        a.stopFlashTitle();
        MMNotification.cancel();
        d.triggerEvent("windowFocus")
    };
    f.onblur = function() {
        e = !1;
        d.triggerEvent("windowBlur")
    };
    a.isWindowFocus = function() {
        return e
    };
    var g = "", i = "", j = !1, l = null, k = d.model("message"), m = [], n = !1, q = a("#vernierContainer .activeChatVernier"), p = null, s = 0, o = !1, r = 0, D = !1, t = null;
    d.createCtrl("chat_conversationListContent", {init:function() {
        var b = this;
        l = a("#conversationContainer");
        p = a("#totalUnreadDot");
        b.getDom$().scrollable({onscroll:function() {
            clearTimeout(s);
            s = setTimeout(function() {
                b._convActive()
            }, 200)
        }})
    }, active:function(a) {
        var b = this;
        e || b.windowFocus();
        (i = a.userName) && d.util.batchgetUndownloadedContact([i]);
        g ? b.conversationListSearch("", function() {
            0 <= b._getUiConvDataIndex(i) ? b._convActive(!0) : d.util.createNewSession(i)
        }) : (b._convActive(!0), a = b._getUiConvDataIndex(i), 0 <= a && (a = m[a]) && !0 == a.invisible && b.focusToTop(i))
    }, _convActive:function(b, c) {
        var e = t && t.attr("un") || "";
        if(i != e || c) {
            t && t.removeClass("activeColumn"), (t = a("#conv_" + a.getAsciiStr(i))).addClass("activeColumn")
        }
        i && d.widget.scrollFocus(this.getDom$().parent(), t, q, b)
    }, chooseConversation:function(b, c) {
        c.addClass("activeColumn");
        var f = this._getUiConvDataIndex(i);
        0 <= f && 0 < m[f].unread && (j = k.markMsgsRead(i), this._handleConvItemDataChangeByUserName(i));
        j && (d.logic("sync").notifyMobile(i, 1), j = !1);
        f = c.attr("userName");
        if(j = k.markMsgsRead(f)) {
            d.logic("sync").notifyMobile(f, 1), j = !1, this._handleConvItemDataChangeByUserName(f)
        }
        if(g) {
            var h = d.model("message").getLastMessage(f);
            h && (h.weight = a.now())
        }
        e = !0;
        a.hash("#chat?userName=" + f)
    }, conversationListSearch:function(b, c) {
        var e = this;
        setTimeout(function() {
            b != g && (g = b, m = d.logic("getconversation").get(a.trim(g)), e._renderList(), e.getDom$().parent().scrollTop(0), c ? c() : e._convActive())
        })
    }, loadMoreConv:function(b, c) {
        for(var e = 0, f = 0, g = m.length;e < g && 10 > f;e++) {
            m[e].invisible && (m[e].invisible = !1, a("#conv_" + a.getAsciiStr(m[e].userName)).show().after(c), f++)
        }
        e == m.length && (n = !0, c.remove());
        d.ossLog({Type:10})
    }, focusToTop:function(a) {
        var b = this._getUiConvDataIndex(a);
        0 < b && this._sortConvAndUpateUi(a, b);
        this._convActive();
        this.getDom$().parent().scrollTop(0)
    }, inited:function() {
        if((m = d.logic("getconversation").get()) && m.length) {
            for(var a = [], b = 0, c = m.length;b < c;b++) {
                a.push(m[b].userName)
            }
            d.util.batchgetUndownloadedContact(a);
            this._renderList();
            i && this._convActive(!0, !0)
        }
    }, _showTitleTip:function() {
        for(var b = r = 0, c = m.length;b < c;b++) {
            r += m[b].unread || 0
        }
        D && r ? p.html(r).show() : p.hide();
        e || (0 < r ? (a.flashTitle(a.tmpl(d.getRes("text_new_message_come"), {count:r})), (b = this._getFirstUnreadConv()) && d.model("account").isNotifyOpen() && MMNotification.notify(b.avatar, a.tmpl(d.getRes("text_new_message_come"), {count:r}), a.subAsiiStr(a.clearHtmlStr(b.name + ": " + (a.clearHtmlStr(b.digest) || d.getRes("text_emoji_replacer"))), 50, "..."), {onclick:function() {
            f.focus()
        }})) : (a.stopFlashTitle(), MMNotification.cancel()))
    }, messageAdded:function(c) {
        d.util.batchgetUndownloadedContactInMesssage([c]);
        var f = d.util.getMsgPeerUserName(c);
        f == i && !o && e && b && k.markMsgsRead(i) && (j = !0);
        var h = this._getUiConvDataIndex(f);
        0 <= h ? (m[h].invisible = !1, this._handleConvItemDataChangeByUserName(f), this._sortConvAndUpateUi(f, h)) : g || (h = d.logic("getconversation").genConversation(f), m[0 < c.CreateTime ? "unshift" : "push"](h), 0 > c.MsgType && (0 > c.CreateTime && 15 < m.length && !n && f != i) && (h.invisible = !0), l[0 < c.CreateTime ? "prepend" : "append"](a.tmpl("chat_conversationItem", h)));
        this._convActive(!0);
        this._showTitleTip()
    }, messageUpdated:function(a) {
        d.util.batchgetUndownloadedContactInMesssage([a]);
        this._handleConvItemDataChangeByUserName(d.util.getMsgPeerUserName(a))
    }, contactUpdated:function(a) {
        this._handleConvItemDataChangeByUserName(a.UserName)
    }, contactAdded:function(a) {
        this.contactUpdated(a)
    }, contactDeleted:function(a) {
        this.sessionDeleted(a.UserName)
    }, sessionDeleted:function(b) {
        var c = this._getUiConvDataIndex(b);
        0 > c || (m.splice(c, 1), a("#conv_" + a.getAsciiStr(b)).remove(), b == i && a.hash("chat"))
    }, noHandledKeyDown:function(b) {
        if(a.isHotkey(b, "down") || a.isHotkey(b, "up")) {
            if(b.stopPropagation(), b.preventDefault(), !a.hash().endsWith("/contactlist")) {
                var c = 0;
                if(i) {
                    for(var d = 0, e = m.length;d < e;d++) {
                        if(m[d].userName == i) {
                            c = d;
                            a.isHotkey(b, "down") && d + 1 < e ? c++ : a.isHotkey(b, "up") && 0 < d && c--;
                            break
                        }
                    }
                    if(m[c].invisible) {
                        return
                    }
                }
                try {
                    if(m[c]) {
                        var f = a("#conv_" + a.getAsciiStr(m[c].userName));
                        f.length && this.chooseConversation(b, f)
                    }
                }catch(g) {
                    alert(g)
                }
                b.stopPropagation();
                b.preventDefault()
            }
        }
    }, _renderList:function() {
        if(!g && !n) {
            for(var b = 15, c = m.length;b < c;b++) {
                m[b].invisible = !0
            }
        }
        l.html(a.tmpl("chat_conversationList", {filter:g, list:m}))
    }, _sortConvAndUpateUi:function(b, d) {
        var e = a("#conv_" + a.getAsciiStr(b));
        e.length && (l.prepend(e), e.show(), d != c && (e = m.splice(d, 1), m.unshift(e[0]), e[0].invisible = !1))
    }, _handleConvItemDataChangeByUserName:function(a) {
        0 <= this._getUiConvDataIndex(a) && this._updateConvUIItem(d.logic("getconversation").genConversation(a))
    }, _updateConvUIItem:function(b) {
        var c = b.userName, d = a("#conv_" + a.getAsciiStr(c));
        if(d.length) {
            var e = this._getUiConvDataIndex(c);
            if(-1 != e) {
                c = d[0].holder;
                c || (d[0].holder = c = {}, c.avatar$ = d.find(".avatar"), c.name$ = d.find(".name"), c.time$ = d.find(".time"), c.mute$ = d.find(".mute"), c.digest$ = d.find(".desc"), c.sendFailedStatus$ = d.find(".sendFailedStatus"), c.sendingStatus$ = d.find(".sendingStatus"), c.unread$ = d.find(".unreadDot"), c.count$ = d.find(".personNum"));
                d = m[e];
                d.avatar != b.avatar && c.avatar$.attr("src", b.avatar);
                d.name != b.name && c.name$.html(b.name);
                d.time != b.time && (c.time$.text(b.time), c.mute$[b.muted ? "show" : "hide"]());
                1 == b.status ? c.sendingStatus$.show() : c.sendingStatus$.hide();
                5 == b.status ? c.sendFailedStatus$.show() : c.sendFailedStatus$.hide();
                d.digest != b.digest && c.digest$.html(b.digest);
                if(d.unread != b.unread) {
                    c.unread$.html(b.unread)[b.unread ? "show" : "hide"]()
                }
                d.isRoom && d.memCount != b.memCount && c.count$.html("(" + b.memCount + ")");
                b.invisible = d.invisible;
                a.extend(d, b)
            }
        }
    }, _getUiConvDataIndex:function(a) {
        for(var b = 0, c = m.length;b < c;++b) {
            if(m[b].userName == a) {
                return b
            }
        }
        return-1
    }, _getFirstUnreadConv:function() {
        for(var a = 0, b = m.length;a < b;++a) {
            if(0 < m[a].unread) {
                return m[a]
            }
        }
    }, setChatPanelStatus:function(a) {
        o = a;
        if(!o) {
            var b = this;
            setTimeout(function() {
                b.chooseConversation({}, b.getDom$().find("div .activeColumn"))
            })
        }
    }, hasUserAction:function(a) {
        if(b = a) {
            this.windowFocus(), h()
        }
    }, windowFocus:function() {
        var a = this;
        i && (j = !0, 0 < d.model("message").getUnreadMsgsCount(i) && setTimeout(function() {
            k.markMsgsRead(i) && a._handleConvItemDataChangeByUserName(i)
        }, 500))
    }, markMsgRead:function(a) {
        this._handleConvItemDataChangeByUserName(a);
        this._showTitleTip()
    }, needShowContactList:function(a) {
        a || p.hide();
        D = a
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = null;
    d.model("contact");
    var e = d.model("message");
    d.model("account");
    var b = 0, h = 0, g = 0, i = a.browser.msie && 9 > a.browser.version ? 300 : 0, j = 0;
    d.createCtrl("chat_chatmsglist", {init:function() {
        this.getDom$().scrollable()
    }, active:function(b) {
        if(b.userName) {
            if(c == b.userName) {
                return!0
            }
            0 != g && (d.getMediaPlayer().jPlayer("stop"), g = 0);
            c = b.userName;
            var e = this;
            clearTimeout(j);
            j = setTimeout(function() {
                e.refresh(true)
            }, i);
            0 < i && e.getDom$().html("")
        }else {
            this.getDom$().html(a.tmpl("chat_chooseConversation"))
        }
    }, refresh:function(b) {
        var e = d.model("message").getMessages(c);
        this._removeNoMsgTip();
        this.getDom$().html(a.tmpl("chat_chatmsglist", e));
        this.getDom$().parent().scrollTop(b ? 1E5 : 0)
    }, messageAdded:function(b) {
        var e = d.util.getMsgPeerUserName(b), f = d.model("contact").getContact(e);
        !b.isSend && (!d.model("account").isMute() && !b.isSysMessage() && 0 == g && f && !f.isMuted() && !f.isBrandContact()) && (b.actualSender == c && a.isWindowFocus() ? d.widget.playNewMsgSound(d.util.isVoiceMsg(b.MsgType) ? 1 : 2) : d.widget.playNewMsgSound(3));
        e == c && (this._removeNoMsgTip(), this.getDom$().append(a.tmpl("chat_chatmsglist", [b])), b = this.getDom$().parent(), b.scrollTop() + b.height() < this.getDom$().height() - 1E3 || b.scrollTop(1E5))
    }, messageUpdated:function(b) {
        d.util.getMsgPeerUserName(b) == c && b.LocalID && this.getDom$().find("[un='item_" + b.LocalID + "']").replaceWith(a.tmpl("chat_chatmsglist", [b]))
    }, contactAdded:function(a) {
        this.contactUpdated(a)
    }, contactUpdated:function(a) {
        this.getDom$().find("img[un='avatar_" + a.UserName + "']").attr("src", d.util.getNormalAvatarUrl(a.UserName));
        var b = d.model("message").getMessages("fmessage");
        if(!(1 > b.length)) {
            for(var c in b) {
                "fmessage" == b[c].FromUserName && b[c].UserName == a.UserName && (this.messageUpdated(b[c]), d.model("message").initMessageQueue(a.UserName))
            }
        }
    }, accountUpdated:function() {
        this.contactUpdated({UserName:d.model("account").getUserName()})
    }, popImg:function(a, b) {
        d.popImage(b, b.attr("rawSrc"))
    }, playVoice:function(a, e) {
        var f = this, i = e.attr("msgid"), j = e.find("[un='voiceStatus']"), p = j.parents(".cloud");
        if(g == i) {
            d.getMediaPlayer().jPlayer("stop"), g = 0
        }else {
            var s = !1;
            clearInterval(b);
            b = setInterval(function() {
                p.animate({opacity:s ? 1 : 0.5}, 200);
                s = !s;
                21 < ++h && clearInterval(b)
            }, 300);
            h = 0;
            d.getMediaPlayer().jPlayer("stop");
            d.setMediaPlayerUICallbacks({onloadstart:function() {
                Log.d("loadstart")
            }, onprogress:function() {
                Log.d("progress");
                (d.getMediaPlayer().lastStatusDom || j).addClass("icoVoice").removeClass("icoVoicePlaying");
                d.getMediaPlayer().lastStatusDom = j;
                0 < b && (clearInterval(b), b = 0, p.stop().css("opacity", 1));
                j.addClass("icoVoicePlaying").removeClass("icoVoice")
            }, onpause:function() {
                Log.d("onpuase");
                0 < b && (clearInterval(b), b = 0, p.stop().css("opacity", 1));
                j.addClass("icoVoice").removeClass("icoVoicePlaying");
                var a = 0 != g && d.model("message").getNextUnreadVoiceMsg(c, i);
                a && setTimeout(function() {
                    f.playVoice(null, f.getDom$().find("[un='cloud_" + a.MsgId + "']"))
                });
                g = 0
            }, onstop:function() {
                this.onpause();
                Log.d("onstop");
                g = 0
            }, onerror:function() {
                clearInterval(b);
                Log.d("onerror")
            }});
            d.getMediaPlayer().jPlayer("setMedia", {mp3:d.getRes("url_host_https") + "/cgi-bin/mmwebwx-bin/webwxgetvoice?msgid=" + i});
            d.getMediaPlayer().jPlayer("play");
            e.find("[un='unread_" + i + "']").hide();
            var o = d.model("message").getMsgById(c, i);
            o && (o.Status = d.Constants.STATE_READ);
            g = i;
            d.ossLog({Type:d.Constants.MMWEBWX_GETVOICE, Cgi:"webwxgetvoice"})
        }
    }, playVideo:function(a, b) {
        var c = b.attr("msgid"), c = {flv:d.getRes("url_host_https") + "/cgi-bin/mmwebwx-bin/webwxgetvideo?type=flv&msgid=" + c, m4v:d.getRes("url_host_https") + "/cgi-bin/mmwebwx-bin/webwxgetvideo?msgid=" + c, poster:d.getRes("url_host_https") + "/cgi-bin/mmwebwx-bin/webwxgetmsgimg?type=slave&MsgID=" + c, download:d.getRes("url_host_https") + "/cgi-bin/mmwebwx-bin/webwxgetvideo?fun=download&msgid=" + c};
        d.playVideo(c);
        d.ossLog({Type:d.Constants.MMWEBWX_GETVOICE, Cgi:"webwxgetvoice"})
    }, downloadMedia:function(a, b) {
        var c = f.onbeforeunload;
        f.onbeforeunload = null;
        location.href = b.attr("url") + ("&fromuser=" + d.model("account").getUserName()) + "&skey=" + d.model("account").getSkey();
        setTimeout(function() {
            f.onbeforeunload = c
        })
    }, _removeNoMsgTip:function() {
        this.getDom$().find("#noMsgTip").remove()
    }, _recompose:function(a) {
        for(var b = 0, c = a.length;b < c;b++) {
            var e = a[b];
            e.avatarTitle = e;
            e.avatarId = e.actualSender;
            e.avatar = d.util.getNormalAvatarUrl(e.actualSender)
        }
    }, loadHistoryMsg:function(a, b) {
        var e = this, f = b.hide().siblings('[un="loading"]').show();
        d.logic("loadHistoryMsg").loadMore(c, function(a) {
            switch(a) {
                case d.Constants.STATE_FAILED:
                    f.hide().siblings('[un="loaderr"]').show();
                    break;
                default:
                    e.refresh(!1)
            }
        })
    }, userVerify:function() {
        a.hash((a.hash() || "chat") + "/popupmsgprofile")
    }, popupMsgProfile:function(b, d) {
        var e = c;
        _sMsgId = d.attr("msgId");
        a.hash((a.hash() || "chat") + "/popupcontactprofile?userName=" + e + "&msgId=" + _sMsgId)
    }, cancelUpload:function(a, b) {
        var c = b.attr("localId");
        d.triggerEvent("cancelUploadByLocalId", c)
    }, resendMsg:function(a, b, f) {
        var g = this, a = f.attr("msgid"), a = e.getMsgById(c, a);
        a.update({Status:1});
        d.logic("sendMsg").resendText(a, {onerror:function(a) {
            "1201" == a && g.alert(d.getRes("text_exit_chatroom"))
        }})
    }, verifyContact:function() {
        d.util.verificationPopup("verification_request", c, this)
    }, verifyUniContacts:function(a, b) {
        var c = b.siblings("span.friends").attr("usernames").split(",");
        d.util.verificationGroupPopup(c, this)
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    function f(a) {
        var b = e.position().left;
        0 < a ? -b + 320 < e.width() && e.css("left", b - 60) : 0 > b && e.css("left", b + 60)
    }
    var c = "", e = null, b = [], h = 0, g, i, j, l, k = "", m = "person", n = null;
    _oFilterContact = {};
    d.createCtrl("createchatroom", {init:function() {
        (e = this.getDom$().find(".selectedListScroll")).bind("mousewheel", function(a, b) {
            f(b)
        });
        this.getDom$().draggable({handle:".titleContainer", cursor:"move"});
        var a = this.getDom$();
        g = a.find(".searchBar").find("input");
        i = a.find(".selectFriendContainer .selectedPanel");
        j = a.find(".selectFriendContainer .friendList");
        l = a.find(".searchClean")
    }, active:function(a) {
        k = a.userName;
        m = "person";
        n = a.func;
        _oFilterContact = {};
        if("add" == n) {
            if(d.util.isRoomContact(k)) {
                for(var a = (a = d.model("contact").getContact(k)) && a.MemberList || [], e = 0, f = a.length;e < f;e++) {
                    _oFilterContact[a[e].UserName] = !0
                }
            }else {
                _oFilterContact[k] = !0
            }
            this.getDom$().find(".choosePersGroup").hide();
            this.getDom$().find(".title span").hide()[1].style.display = ""
        }else {
            this.getDom$().find(".choosePersGroup").show(), this.getDom$().find(".title span").hide().first().show()
        }
        _oFilterContact[d.Constants.SP_CONTACT_FILE_HELPER] = !0;
        c = "";
        d.widget.screenCentral(this.getDom$(), {showMask:!0});
        this.contactListReady(d.logic("contact").hasGotAllContacts());
        b = [];
        this._renderSelectedContacts();
        a = this.getDom$();
        a.find(".selectGroupChat").removeClass("selectedChat");
        a.find(".selectPersChat").addClass("selectedChat")
    }, inactive:function() {
        a("#mask").hide()
    }, contactListReady:function(b) {
        var e = this;
        if("person" == m) {
            var f = d.model("contact").getAllFriendContact(c, !c, _oFilterContact, !0), g = !c && d.model("contact").getAllStarContact(_oFilterContact) || [];
            if(b) {
                for(var i = 0, j = f.length;i < j;i++) {
                    f[i].choosed = !1
                }
                i = 0;
                for(j = g.length;i < j;i++) {
                    g[i].choosed = !1
                }
            }
            var k = a.tmpl("newchatlist", {init:b, contacts:f, starContacts:g});
            h = f.length + g.length;
            setTimeout(function() {
                e.getDom$().find(".selectFriendContainer").show().find(".group").html(k);
                e.getDom$().find(".selectGroupContainer").hide();
                b && e.getDom$().find(".searchBar input").val("")[0].focus()
            })
        }else {
            "group" == m && setTimeout(function() {
                var b = d.logic("contact").getAllSortedGroups(), b = a.tmpl("chatroomlist", {contacts:b});
                e.getDom$().find(".selectFriendContainer").hide();
                e.getDom$().find(".selectGroupContainer").show().find(".group").html(b)
            })
        }
    }, selectContact:function(a, b) {
        var c = this;
        b.attr("id").replace("sel_con_", "");
        (b = b.find(".checkbox")).toggleClass("checked");
        var d = b.hasClass("checked"), c = this;
        c._toggleSelectedContact(b.attr("username"), d);
        c._renderSelectedContacts();
        d && (g.val() && c._cleanSearchInput(), "none" == i.css("display") && c._showSelectedPanel())
    }, unSelectContact:function(b, c) {
        var d = c.attr("username");
        a("#sel_con_" + a.getAsciiStr(d)).click()
    }, cleanSearchWord:function() {
        this._cleanSearchInput()
    }, _toggleSelectedContact:function(a, c) {
        var e = d.model("contact").getContact(a);
        if(e.choosed = c) {
            b.push(e)
        }else {
            e = 0;
            for(len = b.length;e < len;e++) {
                if(b[e].UserName == a) {
                    b.splice(e, 1);
                    break
                }
            }
            0 == b.length && this._hideSelectedPanel()
        }
    }, _renderSelectedContacts:function() {
        var c = this.getDom$().find(".selectedListScroll");
        c.html(a.tmpl("selectcontactlist", b));
        var d = c.find("span:first-child").outerWidth(!0) * b.length;
        c.width(d).css("left", 320 > d ? 0 : 320 - d);
        this.getDom$().find("#selectContactCount").html("(" + b.length + ")")[0 < b.length ? "show" : "hide"]()
    }, _showSelectedPanel:function() {
        j.css("height", "303px");
        i.show()
    }, _hideSelectedPanel:function() {
        i.hide();
        j.css("height", "373px")
    }, _cleanSearchInput:function() {
        l.hide();
        g.val("");
        g.focus();
        c = a.trim("");
        this.contactListReady()
    }, _hasSpecialFriend:function(b) {
        for(var c = b.MemberList, e = "", f = d.model("contact"), g = 0, h = c.length;g < h;++g) {
            var i = c[g];
            i.MemberStatus == d.Constants.MM_MEMBER_BLACKLIST && (i = f.getContact(i.UserName), e += i.NickName || i.Alias || i.UserName, e += " , ")
        }
        e = e.substr(0, e.length - 2);
        0 < e.length && this.alert(a.tmpl("addBlackContactGroupErrTips", {Friends:e}), null, "verificationRequest");
        for(var j = b.ChatRoomName || k, l = [], m, n = "", g = 0, h = c.length;g < h;++g) {
            i = c[g], i.MemberStatus == d.Constants.MM_MEMBER_NEEDVERIFYUSER && l.push(i.UserName)
        }
        m = l.length;
        0 < m ? m < b.MemberCount ? (a.hash("chat?userName=" + j), setTimeout(function() {
            for(var b = 0;b < m;++b) {
                var c = WebMM.model("contact").getContact(l[b]);
                n += (c.NickName || c.Alias || c.UserName) + " , "
            }
            n = n.substr(0, n.length - 2);
            d.model("message").addFakeSysMsg({MsgType:1E4, FromUserName:j, ToUserName:d.model("account").getUserInfo().UserName, Status:d.Constants.STATE_SENT, CreateTime:a.now() / 1E3, Content:a.tmpl("verificationUinGroup", {Friends:n, UserNames:l.join(",")}), unread:!1})
        }, 500)) : d.util.verificationGroupPopup(l, this) : a.hash("chat?userName=" + j)
    }, newsession:function(a) {
        d.util.createNewSession(a);
        d.ossLog({Type:d.Constants.MMWEBWX_NEW_CHAT})
    }, searchContact:function(b, d) {
        var e = this;
        setTimeout(function() {
            if(a.isHotkey(b, "enter")) {
                if(1 == h) {
                    e.getDom$().find(".friendDetail").click();
                    e._cleanSearchInput();
                    return
                }
                g.val() || e.getDom$().find(".chatSend").click()
            }
            c = a.trim(d.val());
            e.contactListReady();
            "" != d.val() ? l.show() : l.hide()
        })
    }, noHandledKeyDown:function(b) {
        a.isHotkey(b, "enter") && !g.val() && this.getDom$().find(".chatSend").click()
    }, createChatRoom:function() {
        var c = this, e = [], f = d.model("account").getUserInfo().UserName;
        c._hideSelectedPanel();
        for(var g = 0, h = b.length;g < h;g++) {
            var i = b[g].UserName;
            i == f && 1 < h || e.push(i)
        }
        0 == e.length ? a.history.back() : 0 < e.length && "add" == n && d.util.isRoomContact(k) ? (d.logic("modChatroom").addMember(k, e.join(","), {onsuccess:function(a) {
            c._hasSpecialFriend(a);
            d.triggerEvent("switchToChatPanel")
        }}), this.close()) : 1 == e.length && "add" != n ? c.newsession(e[0]) : (k && e.push(k), d.logic("createChatRoom").create("", e, {onbefore:function() {
            a.history.back()
        }, onsuccess:function(a) {
            c._hasSpecialFriend(a)
        }, onerror:function(a) {
            -23 == a ? c.alert(d.getRes("text_create_chatroom_exceed_limit_err")) : c.alert(d.getRes("text_create_chatroom_err"))
        }}))
    }, close:function() {
        this._cleanSearchInput();
        this._hideSelectedPanel();
        a.history.back()
    }, scrollLeft:function() {
        f(-1)
    }, scrollRight:function() {
        f(1)
    }, switchTag:function(a, b) {
        b.attr("un") != m && (this.getDom$().find("[click='switchTag']").removeClass("selectedChat"), b.addClass("selectedChat"), m = b.attr("un"), this.contactListReady())
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = "", e = "", b = "", h, g, i;
    d.createCtrl("chat_leftpanel", {init:function() {
        c = "conversation";
        h = a("#chat_conversationListContent").parent();
        g = a("#chat_contactListContent").parent();
        i = a("#conv_search_clean")
    }, active:function(c) {
        !!e != !!c.userName && (this.getDom$().nextAll().css("visibility", c.userName ? "visible" : "hidden"), f.FormData || d.triggerEvent("swfUploaderInit"));
        c.userName != e && (e = c.userName, b && i.isShow() && this.cleanSearchWord("click", null, this.getDom$().find(".chatListSearchInput")), this.switchPanel({}, a("#chooseConversationBtn")))
    }, focusToTop:function() {
        "conversation" != c && this.switchPanel({}, a("#chooseConversationBtn"))
    }, preSearch:function(b) {
        b && a.isHotkey(b, "tab") && (b.preventDefault(), b.stopPropagation())
    }, search:function(e, f, g) {
        b = a.trim(f.val()) || "";
        g.find(".searchClean")[b ? "show" : "hide"]();
        d.triggerEvent("conversation" == c ? "conversationListSearch" : "contactListSearch", b)
    }, cleanSearchWord:function(a, b, c) {
        var d = c.find("input");
        this.search(a, d.val(""), c);
        a && setTimeout(function() {
            d.focus()
        }, 10)
    }, switchPanel:function(e, f) {
        var k = f.attr("un");
        f.siblings().removeClass("active");
        f.addClass("active");
        c != k && (b && i.isShow() && this.cleanSearchWord(null, i, i.parent()), h.scrollTop(0), c = k, "conversation" == c ? (h.show(), g.hide(), d.triggerEvent("needShowContactList", !1)) : (h.hide(), g.show(), a("#conv_search").focus(), d.triggerEvent("needShowContactList", !0)))
    }})
})(jQuery, WebMM, this);
(function(a, d, f, c) {
    function e(a) {
        return"newsapp" != a && "fmessage" != a
    }
    var b = null, h = a("#sendEmojiIcon"), g = a("#screenSnapIcon"), i = a("#sendFileIcon"), j = a("#sendVoiceIcon"), l = a.isiOS();
    !l && i.show();
    h.show();
    !l && g.show();
    var k = {}, m = a.browser.msie ? 300 : 0, n = 0, q = 0, p = 0, s = 0, o = null;
    d.createCtrl("chat_editor", {init:function() {
        var c = this;
        o = c.getDom$().find("textarea");
        a.textAreaResize(o[0], o.height(), 4 * o.height(), function(a) {
            c.getDom$().prev().height(function(b, c) {
                return c - a
            });
            c.getDom$().height(c.getDom$().height() + a)
        });
        o.on("paste", function(b) {
            if(b.originalEvent.clipboardData && b.originalEvent.clipboardData.types && "Files" == b.originalEvent.clipboardData.types[0]) {
                if(b = b.originalEvent.clipboardData.items, !(1 > b.length)) {
                    var e = b[0].getAsFile();
                    e && !(0 >= e.size) && (b = a.getURLFromFile(e)) && f.uploadPreview.setCallback({send:function() {
                        a.uploadFileByForm({target:{files:[a.extend(e, {name:"undefined.jpg"})]}})
                    }}).setImg(b).show()
                }
            }else {
                d.widget.screenSnap.isClipBoardImage() && c._screenSnapUpload()
            }
        }).on("keydown", function(b) {
                c.hotkeySend(b, a(this));
                b.stopPropagation();
                d.touchUserAction()
            }).on("keyup", function(a) {
                a.stopPropagation()
            });
        a.setDragFileUploadOption(function() {
            var a = d.util.getProxyXHR("uploadFrame");
            return a ? a() : new XMLHttpRequest
        }, c._getDragFileUploadUI());
        a.dragFileUpload("dragPanel", function() {
            return d.getRes("url_file") + "/cgi-bin/mmwebwx-bin/webwxuploadmedia?f=json&un=" + b + "&skey=" + d.model("account").getSkey() + "&wxuin=" + d.model("account").getUin()
        }, function() {
            return d.model("account").getBaseRequest().BaseRequest
        }, c._getDragFileUploadCallbacks())
    }, swfUploaderInit:function() {
        var e = this, f = d.widget.swfUploader;
        if(f.isSupport()) {
            var g = a("#uploadFileContainer"), h = a("#swfUploaderContainer");
            g.offset();
            h.css("width", g.width()).css("height", g.height()).css("left", 0).css("top", 0).appendTo(g);
            f.install(h, {onbefore:function() {
                Log.d("onbefore")
            }, onselect:function(c, g) {
                if(10485760 < g.size) {
                    d.ossLog({Type:d.Constants.MMWEBWX_UPLOADMEDIA_TOO_LARGE}), e.alert(d.getRes("text_file_too_large"))
                }else {
                    if(a.isImg(g.name) && 10485760 < g.size) {
                        d.ossLog({Type:d.Constants.MMWEBWX_UPLOADMEDIA_TOO_LARGE}), e.alert(d.getRes("img_too_large"))
                    }else {
                        f.upload(c, d.getRes("url_file") + "/cgi-bin/mmwebwx-bin/webwxuploadmedia?f=json&un=" + b + "&skey=" + d.model("account").getSkey() + "&wxuin=" + d.model("account").getUin(), {uploadmediarequest:JSON.stringify(a.extend(d.model("account").getBaseRequest(), {ClientMediaId:"" + a.now(), TotalLen:0, StartPos:0, DataLen:0, MediaType:4}))});
                        var h = e._addAppMsg(g.name, g.size);
                        k[c] = {toUserName:b, name:g.name, localId:h}
                    }
                }
            }, onprocess:function(b, d) {
                k[b] !== c && a("#progressBar_" + k[b].localId).css("width", 98 * d / 100).parent().parent().css("visibility", "visible")
            }, onsuccess:function() {
            }, onerror:function() {
                Log.e("JS Function: swfUploaderInit, swf upload onerror, arguments: " + arguments)
            }, oncomplete:function(b, f) {
                debug("upload complete idx:" + b + f);
                if(k[b] !== c) {
                    var g = JSON.parse(f), h = k[b];
                    0 == g.BaseResponse.Ret ? e._doSendAppMsg(h.toUserName, h.name, a.extend({MediaId:g.MediaId, StartPos:g.StartPos}, {LocalId:h.localId})) : d.logic("sendMsg").changeSendingMsgStatus(h.toUserName, h.localId, !1);
                    a("#progressBar_" + h.localId).parent().parent().css("visibility", "hidden");
                    delete k[b]
                }
            }})
        }
    }, active:function(c) {
        var f = this, g = b;
        b = c.userName;
        g && d.model("history").inputRecord(g, this.getDom$().find("textarea").val());
        clearTimeout(n);
        n = setTimeout(function() {
            _oContact = d.model("contact").getContact(b);
            1 == p && f.cancelRecord();
            f.getDom$().children(".inputArea").css("visibility", e(b) ? "" : "hidden");
            b != g && (o.val(d.model("history").inputRecord(b)), clearTimeout(q), q = setTimeout(function() {
                a.safe(function() {
                    e(b) && o[0].focus()
                })
            }, 300))
        }, m)
    }, sendImgMsg:function(c, e, f) {
        !b || !d.model("contact").isContactExisted(b) ? this.alert(d.getRes("text_choose_conversation")) : a.isImg(f[0].filename.value) ? (c = a.now(), f[0].msgimgrequest.value = JSON.stringify(a.extend({Msg:{FromUserName:d.model("account").getUserName(), ToUserName:b, Type:3, LocalID:"" + c}}, d.model("account").getBaseRequest())), e = "actionFrame" + c, a("<iframe>").css("display", "none").attr("id", e).attr("name", e).attr("src", "javascript:;").appendTo("body"), f.attr("target", e), f.submit(), f[0].filename.value =
            "", this._sendImgMsg(c)) : this.alert(d.getRes("text_invalid_img_type"))
    }, _sendImgMsg:function(c, e) {
        d.logic("sendMsg").sendImg({LocalID:c, ClientMsgId:c, FromUserName:d.model("account").getUserName(), ToUserName:b, Type:3, FileUrl:e || ""}, function() {
            a("#actionFrame" + c).remove()
        })
    }, _doSendImgMsgByMedia:function(b, c, e) {
        b = a.extend({Msg:{FromUserName:d.model("account").getUserName(), MediaId:e, ToUserName:b, Type:3, LocalID:"" + c}}, d.model("account").getBaseRequest());
        a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxsendmsgimg?fun=async&f=json", b, {onbefore:function() {
        }, onsuccess:function(a) {
            f[c] && f[c](c, a.MsgID)
        }, onerror:function() {
            f[c] && f[c](c, -1);
            Log.e("Cgi: /cgi-bin/mmwebwx-bin/webwxsendmsgimg?fun=async&f=json, JS Function: _doSendImgMsgByMedia, SendImgMsgByMedia error.")
        }})
    }, sendAppMsg:function(c, e, g) {
        if(!b || !d.model("contact").isContactExisted(b)) {
            this.alert(d.getRes("text_choose_conversation"))
        }else {
            if(f.FormData) {
                a.uploadFileByForm(c), g[0].filename.value = ""
            }else {
                var h = this;
                g[0].uploadmediarequest.value = JSON.stringify(a.extend(d.model("account").getBaseRequest(), {ClientMediaId:"" + a.now(), TotalLen:0, StartPos:0, DataLen:0, MediaType:4}));
                g.attr("action", g.attr("url") + "&skey=" + d.model("account").getSkey());
                g.submit();
                var i = a.getFileName(g[0].filename.value);
                g[0].filename.value = "";
                var j = h._addAppMsg(i), k = b;
                f.sendFile = function(b, c) {
                    "0" == b ? h._doSendAppMsg(k, i, a.extend(c, {LocalId:j})) : d.logic("sendMsg").changeSendingMsgStatus(k, j, !1)
                }
            }
        }
    }, hotkeySend:function(b, c) {
        if(a.isHotkey(b, "enter") || a.isHotkey(b, "ctrl+enter") || a.isHotkey(b, "alt+s")) {
            this._sendTextMsg(c), b.stopPropagation(), b.preventDefault()
        }else {
            if(!a.browser.msie && a.isHotkey(b, "alt+enter")) {
                c.insertTextToInput("\n"), b.stopPropagation(), b.preventDefault()
            }else {
                if(a.isHotkey(b, "esc")) {
                    c.blur()
                }else {
                    if((a.isHotkey(b, "up") || a.isHotkey(b, "down")) && !c.val()) {
                        c.blur(), b.stopPropagation(), b.preventDefault()
                    }
                }
            }
        }
    }, sendMsg:function(a, b, c) {
        1 == p ? d.widget.Recorder.getObject().jStopRecording() : this._sendTextMsg(c.find(".chatInput"))
    }, showEmojiPanel:function() {
        var c = d.model("contact").getContact(b);
        d.globalEventSetting({globalIntercept:!0, interceptDom$:a("#emojiPanel").html(a.tmpl("editor_emoji_panel", {isBrandContact:c && c.isBrandContact()})).fadeIn("fast")})
    }, closeEmojiPanel:function() {
        d.globalEventSetting({globalIntercept:!1});
        a("#emojiPanel").fadeOut("fast")
    }, chooseEmoji:function(c) {
        var d = this;
        d.closeEmojiPanel();
        setTimeout(function() {
            d.getDom$().find(".chatInput").insertTextToInput("[" + c.target.title + "]");
            a.safe(function() {
                e(b) && o[0].focus()
            })
        })
    }, chooseSysEmoji:function(c) {
        var d = this;
        d.closeEmojiPanel();
        setTimeout(function() {
            d.getDom$().find(".chatInput").insertTextToInput("<" + c.target.title + ">");
            a.safe(function() {
                e(b) && o[0].focus()
            })
        })
    }, chooseCustomEmoji:function(a) {
        a = a.target.getAttribute("un");
        if(a = d.widget.getTuzkiMd5(a)) {
            this.closeEmojiPanel(), !b || !d.model("contact").isContactExisted(b) ? this.alert(d.getRes("text_choose_conversation")) : (d.logic("sendMsg").sendSysCustomEmoji(b, a), this._focusInput())
        }
    }, chooseEmojiPanel:function(b, c, d) {
        var e = this, f = c.attr("un");
        d.find("a").each(function() {
            var b = a(this), c = b.attr("un");
            c != f ? (b.removeClass("chooseFaceTab"), e.getDom$().find("." + c).hide()) : (b.addClass("chooseFaceTab"), e.getDom$().find("." + c).show())
        })
    }, noHandledClick:function(b) {
        var b = b.target, c = a("#emojiPanel");
        !a.contains(c[0], b) && c.isShow() && this.closeEmojiPanel()
    }, forwardImgMsg:function() {
        Log.d("forwardImgMsg")
    }, downloadImgMsg:function(a) {
        f.open(a.src + "&fun=download")
    }, screenSnap:function() {
        var a = this;
        d.widget.screenSnap.isSupport() ? d.widget.screenSnap.capture({ok:function() {
            a._screenSnapUpload()
        }}) : a.confirm(d.getRes("text_no_install_plug"), {ok:function() {
            d.widget.screenSnap.install()
        }})
    }, _screenSnapUpload:function() {
        var c = this, e = a.now(), g = a.extend({Msg:{FromUserName:d.model("account").getUserName(), ToUserName:b, Type:3, LocalID:"" + e}}, d.model("account").getBaseRequest()), h = f.uploadPreview, i = !1;
        h.setCallback({cancel:function() {
            i = !0
        }}).show();
        d.widget.screenSnap.upload(JSON.stringify(g), function(d) {
            i || (!d.BaseResponse || d.BaseResponse && 0 != d.BaseResponse.Ret ? (c.alert("Snap error.Please check your network."), Log.e("JS Function: _screenSnapUpload, Snap Error.")) : h.setCallback({send:function() {
                g.Msg.MediaId = d.MediaId;
                g.Msg.ToUserName = b;
                a.netQueue().send("/cgi-bin/mmwebwx-bin/webwxsendmsgimg?fun=async&f=json&scene=screenshot", g, {onbefore:function() {
                    c._sendImgMsg(e)
                }, onsuccess:function(a) {
                    f[e] && f[e](e, a.MsgID)
                }, onerror:function() {
                    f[e] && f[e](e, -1);
                    Log.e("Cgi: /cgi-bin/mmwebwx-bin/webwxsendmsgimg?fun=async&f=json&scene=screenshot, JS Function: WebMM.widget.screenSnap.upload, SendMsgImg error.")
                }})
            }}).setImg("/cgi-bin/mmwebwx-bin/webwxpreview?fun=preview&mediaid=" + encodeURIComponent(d.MediaId)).getDom$().attr("mid", d.MediaId))
        })
    }, sendPreviewImg:function(a, b, c) {
        Log.d(c.attr("mid"))
    }, noHandledKeyDown:function(c) {
        a.isHotkey(c, "ctrl+i") ? a.safe(function() {
            e(b) && o[0].focus()
        }) : a.isHotkey(c, "esc") ? this.getDom$().find("textarea")[0].blur() : a.isHotkey(c, "enter") && this.getDom$().find(".chatSend").click()
    }, _sendTextMsg:function(c) {
        var e = this, f = a.trim(c.val());
        0 == f.length ? setTimeout(function() {
            c.val("")[0].focus()
        }) : !b || !d.model("contact").isContactExisted(b) ? e.alert(d.getRes("text_choose_conversation")) : (c.val("")[0].focus(), d.logic("sendMsg").sendText({Msg:{FromUserName:d.model("account").getUserName(), ToUserName:b, Type:1, Content:f}}, {onerror:function(a) {
            "1201" == a && e.alert(d.getRes("text_exit_chatroom"))
        }}))
    }, _getDragFileUploadCallbacks:function() {
        var b = this;
        return{onbefore:function() {
        }, onprogress:function(b, c) {
            a("#progressBar_" + b).css("width", 98 * c).parent().parent().css("visibility", "visible")
        }, onsuccess:function(a, c, d) {
            b._doSendAppMsg(a, c, d)
        }, onerror:function(a, b, c, e) {
            d.logic("sendMsg").changeSendingMsgStatus(c, e, !1);
            Log.e("JS Function: _getDragFileUploadCallbacks, DragFile Upload Error. Status: " + b)
        }, oncomplete:function() {
        }}
    }, _addAppMsg:function(c, e, f) {
        var g = a.now();
        if(a.isImg(c)) {
            return this._sendImgMsg(g, f), g
        }
        c = {FromUserName:d.model("account").getUserName(), ToUserName:b, Type:6, FileName:c, FileSize:e, Status:1, MsgId:g, ClientMsgId:g, LocalID:g, MsgType:49, CreateTime:Math.floor(g / 1E3)};
        d.model("message").addMessages([c]);
        return g
    }, _doSendAppMsg:function(c, e, f) {
        if(a.isImg(e) && !a.isGif(e)) {
            this._doSendImgMsgByMedia(c, f.LocalId, f.MediaId)
        }else {
            if(a.isGif(e)) {
                d.logic("sendMsg").sendCustomGif(b, f)
            }else {
                if(c = d.model("message").getMsgByLocalId(c, f.LocalId)) {
                    a.extend(c, {MediaId:f.MediaId, Content:this._genAppMsgContent(e, f.MediaId, f.StartPos)}), d.logic("sendMsg").sendAppMsg({Msg:c})
                }
            }
        }
    }, _genAppMsgContent:function(b, c, d) {
        return a.tmpl('<appmsg appid="wxeb7ec651dd0aefa9" sdkver=""><title><![CDATA[<#=title#>]]\></title><des></des><action></action><type><#=type#></type><content></content><url></url><lowurl></lowurl><appattach><totallen><#=totalLen#></totallen><attachid><#=attachId#></attachid><fileext><#=ext#></fileext></appattach><extinfo></extinfo></appmsg>', {title:b, ext:a.getExt(b), type:6, totalLen:d, attachId:c})
    }, _getDragFileUploadUI:function() {
        var c = this, e = 0, f = c.getDom$().find("#dragPanel"), g = f.find("div");
        return{ondocover:function() {
            clearTimeout(e);
            "none" == f.css("display") && (g.html(g.attr("outTxt")), f.show())
        }, ondocleave:function() {
            e = setTimeout(function() {
                f.hide()
            }, 500)
        }, ontargetover:function() {
            g.html(g.attr("inTxt"))
        }, ontargetdrop:function(e, g, h) {
            if(!b || !d.model("contact").isContactExisted(b)) {
                c.alert(d.getRes("text_choose_conversation"))
            }else {
                return f.hide(), 10485760 < g ? (d.ossLog({Type:d.Constants.MMWEBWX_UPLOADMEDIA_TOO_LARGE}), c.alert(d.getRes("text_file_too_large")), !1) : a.isImg(e) && 10485760 < g ? (d.ossLog({Type:d.Constants.MMWEBWX_UPLOADMEDIA_TOO_LARGE}), c.alert(d.getRes("img_too_large")), !1) : e ? {localId:c._addAppMsg(e || "", g, h), toUserName:b} : !0
            }
        }, ontargetleave:function() {
            g.html(g.attr("outTxt"))
        }}
    }, sendLocalEmoji:function(c, e, f) {
        if(!b || !d.model("contact").isContactExisted(b)) {
            this.alert(d.getRes("text_choose_conversation"))
        }else {
            if(a.isImg(f[0].filename.value)) {
                var g = a.now();
                f[0].msgimgrequest.value = JSON.stringify(a.extend({Msg:{FromUserName:d.model("account").getUserName(), ToUserName:b, Type:3, LocalID:"" + g}}, d.model("account").getBaseRequest()));
                c = "actionFrame" + g;
                a("<iframe>").css("display", "none").attr("id", c).attr("name", c).attr("src", "javascript:;").appendTo("body");
                f.attr("target", c);
                f.submit();
                f[0].filename.value = "";
                this._sendCustomEmojiMsg(g, "", function() {
                    a("#actionFrame" + g).remove()
                })
            }else {
                this.alert(d.getRes("text_invalid_img_type"))
            }
        }
    }, _sendCustomEmojiMsg:function(a, c, e) {
        d.logic("sendMsg").sendEmoji({LocalID:a, ClientMsgId:a, FromUserName:d.model("account").getUserName(), ToUserName:b, Content:c || "", Type:d.Constants.MM_DATA_EMOJI}, e)
    }, setChatPanelStatus:function(a) {
        a || this._focusInput()
    }, _focusInput:function() {
        setTimeout(function() {
            a.safe(function() {
                e(b) && o[0].focus()
            })
        }, 500)
    }, toggleRecoder:function() {
        var c = this;
        if(d.widget.Recorder.isSupport()) {
            var e = a("#textInput").toggle(), f = a("#recordInput").toggle();
            if(1 == p) {
                p = 0, d.widget.Recorder.getObject().jCancelRecording()
            }else {
                if(2 == p) {
                    p = 0
                }else {
                    p = 0;
                    var g;
                    d.widget.Recorder.install(g = {onReady:function(e) {
                        var g = d.widget.Recorder.getObject().jIsMicroPhoneAvailable();
                        f[0].innerHTML = a.tmpl("voice_recorder", {Status:g});
                        -2 != g && (-1 == g ? e ? c.cancelRecord() : (d.widget.screenCentral(a(d.widget.Recorder.getObject()).parent()), d.widget.Recorder.getObject().jShowSecuritySetting(1)) : d.widget.Recorder.getObject().jStartRecording(6E4, location.protocol + "//" + location.host + "/cgi-bin/mmwebwx-bin/webwxuploadvoice?tousername=" + b + "&type=" + d.Constants.EN_INFORMAT_WAV, b))
                    }, onPermissionChange:function() {
                    }, onSecurityPanelClose:function() {
                        a(d.widget.Recorder.getObject()).parent().css("left", -1E3);
                        g.onReady(!0)
                    }, onRecordStart:function() {
                        p = 1
                    }, onRecordError:function() {
                        Log.e("JS Function: WebMM.widget.Recorder.install, Record Error.")
                    }, onRecordStop:function() {
                    }, onRecordFinish:function(a, b) {
                        1 == p && (c._sendVoice(a, b), e.toggle(), f.toggle(), p = 0)
                    }, onSendError:function(a, b) {
                        Log.e("JS Function: WebMM.widget.Recorder.install, Send Record Msg Error.");
                        1 == p ? (c.cancelRecord(), c.alert("Record Error.")) : d.logic("sendMsg").finishSentAudio(a, b)
                    }, onSendProgress:function() {
                    }, onSendFinish:function(a, b, c) {
                        d.logic("sendMsg").finishSentAudio(b, c, (JSON.parse(a.data) || {}).MsgId)
                    }, onActivityTime:function(a, b) {
                        s = a;
                        var c = f.find(".recordInfo");
                        c.html(c.attr("recording"));
                        f.find(".recordVol").find("span").each(function() {
                            this.style.height = 20 * (b / 100) * Math.random() + "px"
                        });
                        f.find(".recordTime").html(Math.floor(a / 1E3) + "/60")
                    }})
                }
            }
        }else {
            c.alert(d.getRes("text_no_flash_alert"))
        }
    }, cancelRecord:function() {
        p = 2;
        j.click();
        d.widget.Recorder.getObject().jCancelRecording()
    }, _sendVoice:function(a, b) {
        d.logic("sendMsg").sendAudio(a, s, b)
    }, cancelUploadByLocalId:function() {
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = "", c = "", e = !1, b, h = !1;
    d.createCtrl("chat_chattingmgr", {init:function() {
        var a = this.getDom$().find(".section");
        b = a.first().children();
        a.last();
        b.scrollable()
    }, active:function(a) {
        (f = a.userName) && (h || this._render(""))
    }, _render:function(f) {
        if(f != c || h) {
            c = f;
            e = d.util.isRoomContact(f);
            var f = d.model("contact").getContact(f), i = [];
            if(f) {
                if(e) {
                    for(var j = 0, l = f.MemberList && f.MemberList.length;j < l;j++) {
                        var k = f.MemberList[j];
                        i.push(d.model("contact").getContact(k.UserName) || k)
                    }
                }else {
                    i.push(f)
                }
                b.html(a.tmpl("chat_detail_panel", {IsChatroom:e, IsChatroomOwner:f.isRoomOwner(), NickName:f.NickName, Contacts:i}));
                e && (i = this.getDom$().find(".partiTitleName"), i.html(f.NickName || i.attr("noname")));
                a("#chatting_mgr_operator").css("visibility", e ? "visible" : "hidden")
            }else {
                b.html(a.tmpl("chat_detail_panel", {IsChatroom:e, NickName:"", Contacts:[]}))
            }
        }
    }, contactAdded:function(a) {
        this.contactUpdated(a)
    }, contactUpdated:function(b) {
        if(h) {
            if(b.UserName == f) {
                this._render(f)
            }else {
                if(d.util.isRoomContact(f)) {
                    for(var c = d.model("contact").getContact(f), e = (c || {}).MemberList || [], l = 0, k = e.length;l < k;l++) {
                        if(e[l].UserName == b.UserName) {
                            e = a("#personal_info_" + b.UserName);
                            e.length && e.replaceWith(a.tmpl("chat_detail_contact_item", {IsChatroom:!0, IsChatroomOwner:c.isRoomOwner(), Contact:b}));
                            break
                        }
                    }
                }
            }
        }
    }, chatroomMemberFocus:function() {
    }, quitChatroom:function() {
        this.confirm(d.getRes("text_quit_chatroom_alert"), {ok:function() {
            d.logic("modChatroom").quit(f)
        }, cancel:function() {
        }})
    }, modChatroomTopic:function(b, c) {
        var e = this, h = d.model("contact").getContact(f);
        this.getDom$().find(".chatDetailsTitle input").val(h.NickName).show().moveToInputEnd().off("keyup").on("keyup", function(b) {
            if(a.isHotkey(b, "enter") || a.isHotkey(b, "esc")) {
                a.trim(this.value) && (c.html(a.trim(this.value) || c.attr("noname")), e._modTopic(this.value)), this.style.display = "none"
            }
            32 < a.getAsiiStrLen(a.trim(this.value)) && (this.value = a.trim(this.value).substring(0, 32))
        }).off("blur").on("blur", function() {
                a.trim(this.value) && (c.html(a.trim(this.value) || c.attr("noname")), e._modTopic(this.value));
                this.style.display = "none"
            })
    }, _modTopic:function(b) {
        var c = d.model("contact").getContact(f), b = a.trim(b);
        b != c.DisplayName && (c.NickName = b, d.logic("modChatroom").modTopic(f, b))
    }, createChatroom:function() {
        a.hash((a.hash() || "chat") + "/createchatroom?userName=" + f + "&func=add");
        return!1
    }, addChatroomMember:function() {
    }, delChatroomMember:function(a, b) {
        var c = b.attr("un");
        d.logic("modChatroom").delMember(f, c)
    }, setChatPanelStatus:function(a) {
        (h = a) && this._render(f)
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c = "", e = new Image;
    d.createCtrl("modifyavatar", {init:function() {
        var a = this;
        f.uploadAvatarImg = function(d, f) {
            if("0" == d && a._moCropper) {
                var i = f.SecondaryMediaId || f.MediaId;
                c = f.MediaId;
                e.onload = function() {
                    a._moCropper.setImg("/cgi-bin/mmwebwx-bin/webwxpreview?fun=preview&mediaid=" + i);
                    e.onload = null
                };
                e.src = "/cgi-bin/mmwebwx-bin/webwxpreview?fun=preview&mediaid=" + i
            }
            a.getDom$().find(".loadingMask").hide()
        }
    }, active:function() {
        var b = d.model("account").getUserName();
        this.popupWindow(d.getRes("modify_avatar_title"), a.tmpl("modify_avatar_content", {HeadImgFlag:d.model("account").getUserInfo().HeadImgFlag, avatar:d.util.getNormalAvatarUrl(b) + "&type=big"}), !a.browser.msie && a("#accountAvatarWrapper"), {left:150});
        var c = this.getDom$().find(".editBox"), e = this.getDom$().find(".previewBox");
        this._moCropper = new QMImgCropper(c[0], {previewDoms:e});
        this._moCropper.setImg(d.util.getNormalAvatarUrl(b) + "&type=big")
    }, inactive:function() {
        a("#mask").off("click").hide();
        this._moCropper = e.src = null;
        c = ""
    }, close:function() {
        a.hash(a.hash().replace("/modifyavatar", ""))
    }, returnPre:function() {
        var b = this;
        b.getDom$().find(".preAvartor").fadeIn(function() {
            a.transform(b.getDom$().find(".avatarCntr"), b.getDom$().find(".bigAvatarWrapper"))
        })
    }, gotoModify:function(b, c, d) {
        var e = this;
        (function() {
            var b = e.getDom$().find(".previewBox"), c = e.getDom$().find(".avatarCntr");
            a.transform(c, b, function() {
                d.fadeOut()
            })
        })()
    }, uploadAvatarImg:function(b, c, e) {
        b = e[0].filename.value;
        a.trim(b) && (a.isImg(b) ? (b = a.now(), b = a.extend({Msg:{FromUserName:d.model("account").getUserName(), ToUserName:"", Type:3, LocalID:"" + b}}, d.model("account").getBaseRequest()), e[0].msgimgrequest.value = JSON.stringify(b), e.submit(), this.getDom$().find(".loadingMask").show()) : this.alert(d.getRes("modify_avatar_upload_valid")))
    }, cropper:function(a, e) {
        var f = this;
        this._moCropper.getImg();
        var i = this._moCropper.getPos();
        d.logic("modifyavatar").modify(c, i, {onsuccess:function() {
            f.getDom$().find(".loadingMask").hide();
            f.showTips(e.attr("succTips"), !0, {offset:{left:150}});
            f.close()
        }, onerror:function() {
            f.getDom$().find(".loadingMask").hide();
            f.showTips(e.attr("errTips"), !1, {offset:{left:150}})
        }});
        f.getDom$().find(".loadingMask").show()
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f;
    d.createCtrl("popupcontactprofile", {init:function() {
    }, active:function(c) {
        var e = this, b = d.util.isSelf(c.userName);
        c.msgId ? (f = d.model("message").getMsgById(c.userName, c.msgId)) && (f = a.extend(f, f.Contact)) : f = d.model("contact").getContact(c.userName);
        if(f) {
            e.popupWindow(d.getRes("text_friend_detai_info"), a.tmpl("popupConatctProfile", {Avatar:f.HeadImgUrl, MsgType:f.MsgType, MsgId:f.MsgId, AttrStatus:f.AttrStatus, Contact:f, IsSelf:b}), null, {left:150}, {clickMaskHide:!1, onhide:function() {
                e.back()
            }});
            f.MsgType == d.Constants.MM_DATA_VERIFYMSG && e.getDom$().find(".valiMesg").html(a.tmpl("valiMesg", {Contact:f, History:f.History || []}));
            var h = function(b) {
                a("#showPhotoAlbum").html(a.tmpl("profile_show_photoAlbum", {MediaList:b, showNum:3}))
            };
            d.logic("photoalbum").getPhotoAlbumByUserName(f.UserName) ? h(d.model("photoalbum").getMediaListByUserName(f.UserName)) : f.hasPhotoAlbum && f.hasPhotoAlbum() && d.logic("photoalbum").requestPhotoAlbumByUserName(f.UserName, {onsuccess:function() {
                h(d.model("photoalbum").getMediaListByUserName(f.UserName))
            }})
        }else {
            e.back()
        }
    }, inactive:function() {
        a("#mask").off("click").hide()
    }, close:function() {
        a.history.back()
    }, contactAdded:function(a) {
        this.contactUpdated(a)
    }, contactUpdated:function(a) {
        if(f && a.UserName == f.UserName) {
            var e = this.getDom$();
            if(a.isContact()) {
                var b = e.find(".nextStep input:button");
                1 < b.length && (b.first().show(), b.last().hide())
            }
            a.ContactFlag & d.Constants.MM_CONTACTFLAG_BLACKLISTCONTACT && (e = e.find(".blackContact"), e.first().show(), e.last().hide());
            a.isContact() && this.getDom$().find(".remarkSection").is(":hidden") && this.getDom$().find(".remarkSection").show()
        }
    }, messageUpdated:function(c) {
        f && (c.MsgType == d.Constants.MM_DATA_VERIFYMSG && c.RecommendInfo && c.RecommendInfo.UserName == f.UserName) && this.getDom$().find(".valiMesg").html(a.tmpl("valiMesg", {Contact:f, History:f.History || []}))
    }, _showLoading:function(a) {
        this.getDom$().find(".loadingMaskWind")[a ? "show" : "hide"]()
    }, verify:function(a, e, b) {
        var h = this;
        if(f) {
            if(f.MsgType == d.Constants.MM_DATA_VERIFYMSG) {
                a = d.Constants.MM_VERIFYUSER_VERIFYOK
            }else {
                if(f.AttrStatus & WebMM.Constants.MM_STATUS_VERIFY_USER) {
                    b.hide().prev().show().find("input:text").focus();
                    return
                }
                a = d.Constants.MM_VERIFYUSER_ADDCONTACT
            }
            d.logic("userverify").verify(f.UserName, a, "", f.Contact && f.Contact.scene || 0, {onsuccess:function() {
                h._showLoading(!1);
                h.showTips(e.attr("addSuccTips"), !0, {offset:{left:150}})
            }, onerror:function(a) {
                1206 == a ? b.hide().prev().show().find("input:text").focus() : (h._showLoading(!1), h.showTips(e.attr("addErrTips"), !1, {offset:{left:150}}))
            }}, f.Ticket);
            h._showLoading(!0)
        }
    }, enterRequest:function(c, d, b) {
        a.isHotkey(c, "enter") ? this.sendRequest(c, b.find("input:button").first(), b) : 40 < a.getAsiiStrLen(a.trim(d.val())) && (d.val(a.subAsiiStr(d.val(), 40)), c.preventDefault())
    }, sendRequest:function(c, e, b) {
        var h = this;
        f && (c = a.trim(b.find("input:text").val()), d.logic("userverify").verify(f.UserName, d.Constants.MM_VERIFYUSER_SENDREQUEST, c, f.Contact && f.Contact.scene || 0, {onsuccess:function() {
            h._showLoading(!1);
            h.showTips(e.attr("addSuccTips"), !0, {offset:{left:150}});
            b.hide().next().show()
        }, onerror:function() {
            h._showLoading(!1);
            h.showTips(e.attr("addErrTips"), !1, {offset:{left:150}})
        }}, f.Ticket), h._showLoading(!0))
    }, cancelRequest:function(a, d, b) {
        b.hide().next().show()
    }, showHDAvatar:function(a, d) {
        function b() {
            var a = d.position();
            g.css({width:d.width(), height:d.height(), left:a.left, top:a.top});
            f.fadeIn(function() {
            })
        }
        var f = this.getDom$().find(".hdAvatarContainer"), g = f.find("img"), i = d.attr("src") + "&type=big";
        g.attr("src") ? b() : (g[0].onload = function() {
            b()
        }, g.attr("src", i))
    }, returnToProfile:function(a, d, b) {
        b.fadeOut()
    }, showPhotoAlbum:function(c, d) {
        this.close();
        var b = d.attr("userName");
        a.hash((a.hash() || "chat") + "/popupphotoalbum?userName=" + b);
        return!1
    }, _editTextWithInput:function(c, d, b, f) {
        function g() {
            var g = a.trim(d.val());
            g == i ? (d.hide(), c.show(), f && f.onerror && f.onerror(g)) : (a.getAsiiStrLen(g) > b && (g = a.stripStr(g, b)), d.val(g).hide(), c.text(g).val(g).show(), f && f.onsuccess && f.onsuccess(g))
        }
        var i = c.text() || c.val(), b = b || 16;
        c.hide();
        i && d.val(i);
        d.show();
        a.selectText(d[0]);
        a.setInputLength(d, b).off("keyup").on("keyup", function(b) {
            (a.isHotkey(b, "enter") || a.isHotkey(b, "esc")) && g()
        }).off("blur").on("blur", function() {
                g()
            })
    }, editRemarkName:function(a, e) {
        var b = e.siblings("input");
        b.val() || b.val(b.attr("nickname"));
        e.hide();
        this._editTextWithInput(e.find("span").first(), e.siblings("input"), 32, {onsuccess:function(a) {
            e.show();
            d.logic("oplog").setRemarkName(f.UserName, a);
            "" == a ? e.find("span.editRemarkNameIcon").addClass("show") : e.find("span.editRemarkNameIcon").removeClass("show")
        }, onerror:function() {
            e.show()
        }})
    }, onEditNickName:function(a, d) {
        this._editTextWithInput(d, d.siblings("input"), 16, {onsuccess:function() {
        }})
    }, onEditSignature:function(a, d) {
        this._editTextWithInput(d, d.siblings("textarea"), 30, {onsuccess:function() {
        }})
    }, blackContact:function() {
        this.confirm(a.tmpl("black_contact_confirm"), {ok:function() {
            d.logic("oplog").blackContact(f.UserName, d.Constants.MMWEBWX_OPLOG_BLACKCONTACT_ADD)
        }})
    }, replyVerifyMsg:function(a, e) {
        var b = e.attr("msgid"), h = e.attr("ticket"), g = e.attr("opcode");
        d.util.verificationPopup("verification_reply", f, this, {onsuccess:function(a) {
            var c = d.model("message").getMsgById("fmessage", b), e = c.History;
            e.push("1" + a);
            c.update(e)
        }}, {notEmpty:!0, type:g == d.Constants.MM_VERIFYUSER_SENDREQUEST || g == d.Constants.MM_VERIFYUSER_SENDERREPLY ? d.Constants.MM_VERIFYUSER_RECVERREPLY : d.Constants.MM_VERIFYUSER_SENDERREPLY, ticket:h})
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    var f = "", c = "", e = !1, b = !1, h = !1, g = !1;
    d.createCtrl("chat_contactListContent", {init:function() {
        this.getDom$().scrollable()
    }, active:function(b) {
        f = b.userName;
        g && (this.getDom$().find("a.activeColumn").removeClass("activeColumn"), (b = b.child && b.child.userName) && a("#con_item_" + a.getAsciiStr(b)).addClass("activeColumn"))
    }, contactListReady:function() {
        e = !0;
        b && this._contactListRender(!1)
    }, needShowContactList:function(a) {
        b = !0;
        (g = a) && this._contactListRender(!e)
    }, contactUpdated:function(b) {
        a("#con_item_{0}".format(a.getAsciiStr(b.UserName))).replaceWith(a.tmpl("contactItem", {contact:b}))
    }, _contactListRender:function(b, e) {
        if(!h || e) {
            var g = d.model("contact").getAllFriendContact(c, !c, {}, !c), k = !c && d.model("contact").getAllStarContact() || [], m = d.model("contact").getAllFriendChatroomContact(c) || [], n = !c && d.model("contact").getAllBrandContact() || [], q = this, p = a.tmpl("contactlist", {init:b, curUserName:f, isSearch:!!c, contacts:g, starContacts:k, roomContacts:m, brandContacts:n});
            setTimeout(function() {
                q.getDom$().find("#contactListContainer").html(p)
            });
            b || (h = !0)
        }
    }, contactListSearch:function(a) {
        c = a;
        this._contactListRender(!1, !0);
        this.getDom$().parent().scrollTop(0)
    }, toggleBrandList:function(a, b) {
        b.next(".groupDetail").toggle();
        b.find(".lapIcon").toggleClass("lapedIcon")
    }})
})(jQuery, WebMM, this);
(function(a, d, f) {
    var c, e, b, h, g, i, j, l, k, m, n, q, p, s, o, r, D, t, C, A, v, y, w, F, B, E, G, u = [], z, x, H, I, K, L, J;
    d.createCtrl("popupphotoalbum", {active:function(b) {
        var c = this;
        x = b.userName;
        c._photoAlbumInit();
        z.hide();
        d.widget.screenCentral(z.parent(), a.extend({showMask:!0, lightMask:!1}));
        z.stop(!0).fadeIn("fast");
        if(b = d.logic("photoalbum").getPhotoAlbumByUserName(x)) {
            c.photoAlbumLoaded(b), c._requestMedia()
        }else {
            return c._requestMedia({success:function(a, b) {
                c.photoAlbumLoaded(b)
            }, error:function(a) {
                Log.d("Cannot get " + a + "'s photo album");
                c.alert("Load photoalbum error, please try again.")
            }}), !1
        }
    }, inactive:function() {
        a("#mask").off("click").hide()
    }, close:function() {
        a("#mask").off("click").hide();
        a.history.back()
    }, _photoAlbumInit:function() {
        var c = this, d = c.getDom$();
        if(0 >= d.children("#popupPhotoAlbumWindow").length) {
            d.css("visibility", "hidden");
            d.html(a.tmpl("popupPhotoAlbumWindow", ""));
            var e = a("<li/>");
            m = a("#popupPhotoAlbum_thumbList").append(e);
            p = e.outerWidth(!0);
            z = this.getDom$().children("#popupPhotoAlbumWindow");
            z.find(".closePart").css("visibility", "hidden");
            d.css("visibility", "visible");
            e.remove();
            D = [];
            b = d.find(".popupPhotoAlbumPanel");
            h = b.find(".friendCirLPanel");
            g = b.find(".friendCirRPanel");
            y = a("#popupPhotoAlbum_photoView");
            k = a("#nextThumbLoading");
            i = a("#thumbPreView");
            w = y.children("img");
            A = a("#prevPhoto");
            v = a("#nextPhoto");
            j = a("#prevThumb");
            l = a("#nextThumb");
            a("#photoViewLeftPanel").hover(function() {
                A.parent().toggle()
            });
            a("#photoViewRightPanel").hover(function() {
                v.parent().toggle()
            });
            m.delegate("li", "mouseenter", function() {
                c.thumbPreViewShow(a(this))
            }).delegate("li", "mouseleave", function() {
                    c.thumbPreViewHide(a(this))
                });
            w.on("mousewheel", function(a, b) {
                c._photoZoom(a, b)
            }).draggable({distance:0})
        }
        a(f).bind("resize", function() {
            c._resize()
        });
        this._photoAlbumInit = function() {
        }
    }, _photoZoom:function(a, b) {
        var c = w.width(), d = w.height(), e = (10 + b) / 10, f = c * e, e = d * e, g = parseInt(w.css("left")), h = parseInt(w.css("top"));
        w.css({width:f, height:e, left:g - (f - c) * a.offsetX / c, top:h - (e - d) * a.offsetY / d})
    }, _showPhotoAlbum:function() {
        var a = this.getDom$();
        a.isShow() && a.find(".closePart").css("visibility", "visible")
    }, _updataPhotoAlbum:function(b, c) {
        for(var d = 0, e = b.length;d < e;++d) {
            var f = "popupPhotoAlbum_" + b[d];
            a("#" + f).html(a.tmpl(f, c))
        }
    }, _changeAlbum:function(a) {
        if(c != a) {
            var b = e[a];
            if(b) {
                this._updataPhotoAlbum(["albumInfo", "commentList", "albumContent", "albumDate"], {Album:b, ObjectDesc:b.ObjectDesc});
                var b = this.getDom$().find(".popupPhotoAlbum_albumMonth"), d = b.eq(0).text();
                b.eq(1).text(d);
                c = a;
                this._resizeCommentList()
            }
        }
    }, _setPhotoSize:function(a, b) {
        var c = a / b, d, e;
        a <= F && b <= B ? (d = a, e = b) : c > E ? (d = "100%", e = "auto", a = F, b = a / c) : c < E && (d = "auto", b = e = B, a = b * c);
        w.css({width:d, height:e, left:(F - a) / 2, top:(B - b) / 2})
    }, _changePhoto:function(a) {
        var b = this, c = parseInt(a.attr("w")), d = parseInt(a.attr("h"));
        w.attr({w:c, h:d});
        w.stop(!0).fadeOut(200, function() {
            b._setPhotoSize(c, d);
            w.attr("src", a.attr("url")).stop(!0).fadeIn(200, function() {
                G && b._showPhotoAlbum()
            })
        });
        this._preLoadPhoto(3)
    }, _changeThumb:function(a) {
        if(!a.hasClass("on") && a && !(1 > a.length)) {
            a.addClass("on").siblings().removeClass("on");
            var b = parseInt(a.attr("albumindex")), d = a.index();
            this._changePhoto(a);
            b != c && this._changeAlbum(b);
            0 >= d ? A.hide() : A.show();
            d < o ? v.show() : v.hide();
            C || (a = a.position().left - m.position().left, this._scrollThumbNum(Math.round((a - this.getDom$().find(".photoPreListBox").width() / 2) / p)))
        }
    }, _hasMoreMedia:function() {
        return o < u.length - 1 || !WebMM.model("photoalbum").getLoadAllByUserName(x)
    }, _LoadMoreMedia:function(a, b) {
        clearTimeout(I);
        l.hide();
        k.show();
        var c = this;
        o + a > u.length - 1 && !WebMM.model("photoalbum").getLoadAllByUserName(x) ? 0 != H ? I = setTimeout(function() {
            c._LoadMoreMedia(a, b)
        }, 1E3) : c._requestMedia({success:function() {
            c._AddMoreMediaFinish(a, b)
        }, error:function() {
            clearTimeout(I);
            k.hide();
            l.show();
            c.alert("Load photoalbum error, please try again.")
        }}) : c._AddMoreMediaFinish(a, b)
    }, _AddMoreMediaFinish:function(b, c) {
        var d = n && n.length || 0;
        m.append(a.tmpl("popupPhotoAlbum_thumbList", {MediaList:u, StartIndex:d, LoadNum:b}));
        n = m.children("li");
        for(var e = n.length;d < e;++d) {
            D.push(n.eq(d).find("img"))
        }
        this._loadThumbStack();
        o = n.length - 1;
        m.css({width:p * n.length});
        k.hide();
        l.show();
        c && c();
        o + r >= u.length - 1 && this._requestMedia()
    }, _requestMedia:function(a) {
        if(!WebMM.model("photoalbum").getLoadAllByUserName(x)) {
            H++;
            var b = this;
            d.logic("photoalbum").requestPhotoAlbumByUserName(x, {onsuccess:function(c, d) {
                var f = WebMM.model("photoalbum");
                e = f.getByUserName(c).ObjectList;
                u = f.getMediaListByUserName(c);
                a && a.success && a.success(c, d);
                2 > H ? b._requestMedia() : H = 0
            }, onerror:function(b) {
                a && a.error && a.error(b)
            }})
        }
    }, _preLoadThumb:function(a) {
        clearTimeout(K);
        K = setTimeout(function() {
            a || (a = r);
            for(var b = u.length - 1 - o, b = b < a ? b : a;0 < b;--b) {
                (new Image).src = u[o + b].thumb
            }
        }, 1E3)
    }, _preLoadPhoto:function(a) {
        clearTimeout(L);
        L = setTimeout(function() {
            a || (a = r);
            for(var b = n.filter(".on").index(), c = u.length - 1 - b, c = c < a ? c : a, d = 1;d <= c;++d) {
                (new Image).src = u[b + d].url
            }
            setTimeout(function() {
                for(var a = 1;a <= c;++a) {
                    var d = b - a;
                    if(0 > d) {
                        break
                    }
                    (new Image).src = u[d].url
                }
            }, 500)
        }, 500)
    }, _loadThumbStack:function() {
        clearInterval(t);
        t = setInterval(function() {
            var a = D.pop();
            a ? a.attr("src", a.attr("loadsrc")) : clearInterval(t)
        }, 50)
    }, _scrollThumbNum:function(a) {
        if(0 != a) {
            var b = this, c;
            c = s + a;
            l.show();
            if(0 < a) {
                if(c >= o) {
                    if(b._hasMoreMedia()) {
                        b._LoadMoreMedia(a + 1, function() {
                            b._scrollThumbNum(a)
                        });
                        return
                    }
                    c = o + 1;
                    l.hide()
                }
            }else {
                c < r - 1 && (c = r - 1)
            }
            s = c > o ? o : c;
            c = -(c - (r - 1)) * p;
            0 == c ? j.hide() : j.show();
            var d = "animate";
            Math.abs(a) > r && (d = "css");
            m.stop(!0, !0)[d]({"margin-left":c});
            b._preLoadThumb()
        }
    }, _resizeCommentList:function() {
        var c = b.height() - parseInt(g.css("padding-top")) - parseInt(g.find(".friendMsg").css("margin-top")) - g.find(".info").outerHeight(!0) - g.find(".praise").outerHeight(!0) - g.find(".comments").children(".title").outerHeight(!0) - 20;
        a("#popupPhotoAlbum_commentList").css("height", c)
    }, _resize:function() {
        q = this.getDom$().find(".photoPreListBox").width();
        F = y.width();
        B = b.height() - (h.outerHeight(!0) - h.height()) - h.find(".photoPreView").outerHeight(!0) - h.find("#popupPhotoAlbum_albumDate").outerHeight(!0);
        y.css("height", B);
        E = F / B;
        r = Math.ceil(q / p);
        this._setPhotoSize(parseInt(w.attr("w")), parseInt(w.attr("h")));
        this._resizeCommentList()
    }, photoAlbumLoaded:function(a) {
        this.getDom$().isShow() && (e = a.ObjectList, c = -1, H = 0, this._resize(), u = WebMM.model("photoalbum").getMediaListByUserName(x), s = o = r < u.length ? r - 1 : u.length - 1, m.html(""), n = null, this._LoadMoreMedia(r), m.css({margin:"0 auto"}), this._changeAlbum(c), G = !0, n.eq(0).children("a").click(), j.hide(), this._hasMoreMedia() ? (l.show(), C = !1) : (l.hide(), C = !0))
    }, noHandledKeyDown:function(b) {
        "none" != A.css("display") && a.isHotkey(b, "left") && A.click();
        "none" != v.css("display") && a.isHotkey(b, "right") && v.click()
    }, closePhotoAlbum:function() {
        var a = this;
        D = [];
        z.stop(!0).fadeOut("fast", function() {
            a.close();
            a.getDom$().find(".closePart").css("visibility", "hidden");
            z.hide()
        })
    }, prevPhoto:function() {
        this._changeThumb(n.filter(".on").prev())
    }, nextPhoto:function() {
        this._changeThumb(n.filter(".on").next())
    }, thumbClick:function(a, b) {
        this.thumbPreViewHide();
        this._changeThumb(b.parents("li"))
    }, thumbPreViewShow:function(a) {
        clearTimeout(J);
        i.children("img").attr("src", a.find("img").attr("src"));
        J = setTimeout(function() {
            i.css({top:-i.outerHeight(!0) - 20 + "px", left:a.position().left - (i.outerWidth(!0) - a.children("a").outerWidth()) / 2 + "px"});
            i.fadeIn(200)
        }, 300)
    }, thumbPreViewHide:function() {
        clearTimeout(J);
        i.hide()
    }, prevThumb:function() {
        this._scrollThumbNum(-(r - 1))
    }, nextThumb:function() {
        this._scrollThumbNum(r - 1)
    }, toggleAlbumContent:function(a, b) {
        b.hasClass("showAll") ? b.removeClass("showAll") : b.addClass("showAll")
    }, showAllLike:function(b, c) {
        var d = a("#popupPhotoAlbum_likeList").parent();
        d.hasClass("showAll") ? (d.removeClass("showAll"), c.text(c.attr("unfoldtext"))) : (c.attr("unfoldtext", c.text()), c.text(c.attr("foldtext")), d.addClass("showAll"));
        this._resizeCommentList()
    }, resize:function() {
    }})
})(jQuery, WebMM, this);
(function(a, d) {
    d.createCtrl("feedback", {active:function() {
        this.popupWindow(this.getDom$().attr("_title"), a.tmpl("feedback", {}), null, {left:150});
        this.getDom$().find(".left").html(this.getDom$().find("textarea").focus().attr("maxlength"))
    }, inactive:function() {
        a("#mask").off("click").hide()
    }, close:function() {
        a.history.back()
    }, edit:function() {
        return!1
    }, send:function(a, c, e) {
        a = e.find("textarea");
        if(c = a.val().trim()) {
            d.logic("feedback").send(c), this.showTips(a.attr("tips"), !0)
        }
        this.close()
    }})
})(jQuery, WebMM);


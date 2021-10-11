/*
 *  jQuery screen skeleton - scheletrone - v1.0.6
 *  A jQuery plugin to make a skeleton loading of your html elements.
 *
 *  GitHub: https://github.com/enbifa/jquery.skeleton.loader
 *  Copyright (c) 2017 - Vincenzo Bifano
 */


;(function ( $, window, document ) {
'use strict';

    var debugLog = false;
    var IdElement = "";
    var Name = 'scheletrone';
    var ReplaceText;
    var Words = [
        "lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit", "ut", "aliquam,", "purus", "sit", "amet", "luctus", "venenatis,", "lectus", "magna", "fringilla", "urna,", "porttitor", "rhoncus", "dolor", "purus", "non", "enim", "praesent", "elementum", "facilisis", "leo,", "vel", "fringilla", "est", "ullamcorper", "eget", "nulla", "facilisi", "etiam", "dignissim", "diam", "quis", "enim", "lobortis", "scelerisque", "fermentum", "dui", "faucibus", "in", "ornare", "quam", "viverra", "orci", "sagittis", "eu", "volutpat", "odio", "facilisis", "mauris", "sit", "amet", "massa", "vitae", "tortor", "condimentum", "lacinia", "quis", "vel", "eros", "donec", "ac", "odio", "tempor", "orci", "dapibus", "ultrices", "in", "iaculis", "nunc", "sed", "augue", "lacus,", "viverra", "vitae", "congue", "eu,", "consequat", "ac", "felis", "donec", "et", "odio", "pellentesque", "diam", "volutpat", "commodo", "sed", "egestas", "egestas", "fringilla", "phasellus", "faucibus", "scelerisque", "eleifend", "donec", "pretium", "vulputate", "sapien", "nec", "sagittis", "aliquam", "malesuada", "bibendum", "arcu", "vitae", "elementum",
        "curabitur", "vitae", "nunc", "sed", "velit", "dignissim", "sodales", "ut", "eu", "sem", "integer", "vitae", "justo", "eget", "magna", "fermentum", "iaculis", "eu", "non", "diam", "phasellus", "vestibulum", "lorem", "sed", "risus", "ultricies", "tristique", "nulla", "aliquet", "enim", "tortor,", "at", "auctor", "urna", "nunc", "id", "cursus", "metus", "aliquam", "eleifend", "mi", "in", "nulla", "posuere", "sollicitudin", "aliquam", "ultrices", "sagittis", "orci,", "a", "scelerisque", "purus", "semper", "eget", "duis", "at", "tellus", "at", "urna", "condimentum", "mattis", "pellentesque", "id", "nibh", "tortor,", "id", "aliquet", "lectus", "proin", "nibh", "nisl,", "condimentum", "id", "venenatis", "a,", "condimentum", "vitae", "sapien", "pellentesque", "habitant", "morbi", "tristique", "senectus", "et", "netus", "et", "malesuada", "fames", "ac", "turpis", "egestas", "sed", "tempus,", "urna", "et", "pharetra", "pharetra,", "massa", "massa", "ultricies", "mi,", "quis", "hendrerit", "dolor", "magna", "eget", "est", "lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit", "pellentesque", "habitant", "morbi", "tristique", "senectus", "et", "netus", "et", "malesuada", "fames", "ac", "turpis", "egestas", "integer", "eget", "aliquet", "nibh", "praesent", "tristique", "magna", "sit", "amet", "purus", "gravida", "quis", "blandit", "turpis", "cursus", "in", "hac", "habitasse", "platea", "dictumst", "quisque", "sagittis,", "purus", "sit", "amet", "volutpat", "consequat,", "mauris", "nunc", "congue", "nisi,", "vitae", "suscipit", "tellus", "mauris", "a", "diam",
        "maecenas", "sed", "enim", "ut", "sem", "viverra", "aliquet", "eget", "sit", "amet", "tellus", "cras", "adipiscing", "enim", "eu", "turpis", "egestas", "pretium", "aenean", "pharetra,", "magna", "ac", "placerat", "vestibulum,", "lectus", "mauris", "ultrices", "eros,", "in", "cursus", "turpis", "massa", "tincidunt", "dui", "ut", "ornare", "lectus", "sit", "amet", "est", "placerat", "in", "egestas", "erat", "imperdiet", "sed", "euismod", "nisi", "porta", "lorem", "mollis", "aliquam", "ut", "porttitor", "leo", "a", "diam", "sollicitudin", "tempor", "id", "eu", "nisl", "nunc", "mi", "ipsum,", "faucibus", "vitae", "aliquet", "nec,", "ullamcorper", "sit", "amet", "risus", "nullam", "eget", "felis", "eget", "nunc", "lobortis", "mattis", "aliquam", "faucibus", "purus", "in", "massa", "tempor", "nec", "feugiat", "nisl", "pretium", "fusce", "id", "velit", "ut", "tortor", "pretium", "viverra", "suspendisse", "potenti", "nullam", "ac", "tortor", "vitae", "purus", "faucibus", "ornare", "suspendisse", "sed", "nisi", "lacus,", "sed", "viverra", "tellus", "in", "hac", "habitasse", "platea", "dictumst", "vestibulum", "rhoncus", "est", "pellentesque", "elit", "ullamcorper", "dignissim", "cras", "tincidunt", "lobortis", "feugiat", "vivamus", "at", "augue", "eget", "arcu", "dictum", "varius", "duis", "at", "consectetur", "lorem",
        "donec", "massa", "sapien,", "faucibus", "et", "molestie", "ac,", "feugiat", "sed", "lectus", "vestibulum", "mattis", "ullamcorper", "velit", "sed", "ullamcorper", "morbi", "tincidunt", "ornare", "massa,", "eget", "egestas", "purus", "viverra", "accumsan", "in", "nisl", "nisi,", "scelerisque", "eu", "ultrices", "vitae,", "auctor", "eu", "augue", "ut", "lectus", "arcu,", "bibendum", "at", "varius", "vel,", "pharetra", "vel", "turpis", "nunc", "eget", "lorem", "dolor,", "sed", "viverra", "ipsum", "nunc", "aliquet", "bibendum", "enim,", "facilisis", "gravida", "neque", "convallis", "a", "cras", "semper", "auctor", "neque,", "vitae", "tempus", "quam", "pellentesque", "nec", "nam", "aliquam", "sem", "et", "tortor", "consequat", "id", "porta", "nibh", "venenatis", "cras", "sed", "felis", "eget", "velit", "aliquet", "sagittis", "id", "consectetur", "purus", "ut", "faucibus", "pulvinar", "elementum", "integer", "enim", "neque,", "volutpat", "ac", "tincidunt", "vitae,", "semper", "quis", "lectus", "nulla", "at", "volutpat", "diam", "ut", "venenatis", "tellus", "in", "metus", "vulputate", "eu", "scelerisque", "felis", "imperdiet", "proin", "fermentum", "leo", "vel", "orci", "porta", "non", "pulvinar", "neque", "laoreet", "suspendisse", "interdum", "consectetur", "libero,", "id", "faucibus", "nisl", "tincidunt", "eget", "nullam", "non", "nisi", "est,", "sit", "amet", "facilisis", "magna",
        "etiam", "tempor,", "orci", "eu", "lobortis", "elementum,", "nibh", "tellus", "molestie", "nunc,", "non", "blandit", "massa", "enim", "nec", "dui", "nunc", "mattis", "enim", "ut", "tellus", "elementum", "sagittis", "vitae", "et", "leo", "duis", "ut", "diam", "quam", "nulla", "porttitor", "massa", "id", "neque", "aliquam", "vestibulum", "morbi", "blandit", "cursus", "risus,", "at", "ultrices", "mi", "tempus", "imperdiet", "nulla", "malesuada", "pellentesque", "elit", "eget", "gravida", "cum", "sociis", "natoque", "penatibus", "et", "magnis", "dis", "parturient", "montes,", "nascetur", "ridiculus", "mus", "mauris", "vitae", "ultricies", "leo", "integer", "malesuada", "nunc", "vel", "risus", "commodo", "viverra", "maecenas", "accumsan,", "lacus", "vel", "facilisis", "volutpat,", "est", "velit", "egestas", "dui,", "id", "ornare", "arcu", "odio", "ut", "sem", "nulla", "pharetra", "diam", "sit", "amet", "nisl", "suscipit", "adipiscing", "bibendum", "est", "ultricies", "integer", "quis", "auctor", "elit",
        "sed", "vulputate", "mi", "sit", "amet", "mauris", "commodo", "quis", "imperdiet", "massa", "tincidunt", "nunc", "pulvinar", "sapien", "et", "ligula", "ullamcorper", "malesuada", "proin", "libero", "nunc,", "consequat", "interdum", "varius", "sit", "amet,", "mattis", "vulputate", "enim", "nulla", "aliquet", "porttitor", "lacus,", "luctus", "accumsan", "tortor", "posuere", "ac", "ut", "consequat", "semper", "viverra", "nam", "libero", "justo,", "laoreet", "sit", "amet", "cursus", "sit", "amet,", "dictum", "sit", "amet", "justo", "donec", "enim", "diam,", "vulputate", "ut", "pharetra", "sit", "amet,", "aliquam", "id", "diam", "maecenas", "ultricies", "mi", "eget", "mauris", "pharetra", "et", "ultrices", "neque", "ornare", "aenean", "euismod", "elementum", "nisi,", "quis", "eleifend", "quam", "adipiscing", "vitae", "proin", "sagittis,", "nisl", "rhoncus", "mattis", "rhoncus,", "urna", "neque", "viverra", "justo,", "nec", "ultrices", "dui", "sapien", "eget", "mi", "proin", "sed", "libero", "enim,", "sed", "faucibus", "turpis", "in", "eu", "mi", "bibendum", "neque", "egestas", "congue", "quisque", "egestas", "diam", "in", "arcu", "cursus", "euismod", "quis", "viverra", "nibh", "cras", "pulvinar", "mattis", "nunc,", "sed", "blandit", "libero", "volutpat", "sed", "cras", "ornare", "arcu", "dui", "vivamus", "arcu", "felis,", "bibendum", "ut", "tristique", "et,", "egestas", "quis", "ipsum", "suspendisse", "ultrices", "gravida", "dictum",
        "fusce", "ut", "placerat", "orci", "nulla", "pellentesque", "dignissim", "enim,", "sit", "amet", "venenatis", "urna", "cursus", "eget", "nunc", "scelerisque", "viverra", "mauris,", "in", "aliquam", "sem", "fringilla", "ut", "morbi", "tincidunt", "augue", "interdum", "velit", "euismod", "in", "pellentesque", "massa", "placerat", "duis", "ultricies", "lacus", "sed", "turpis", "tincidunt", "id", "aliquet", "risus", "feugiat", "in", "ante", "metus,", "dictum", "at", "tempor", "commodo,", "ullamcorper", "a", "lacus", "vestibulum", "sed", "arcu", "non", "odio", "euismod", "lacinia", "at", "quis", "risus", "sed", "vulputate", "odio", "ut", "enim", "blandit", "volutpat", "maecenas", "volutpat", "blandit", "aliquam", "etiam", "erat", "velit,", "scelerisque", "in", "dictum", "non,", "consectetur", "a", "erat", "nam", "at", "lectus", "urna", "duis", "convallis", "convallis", "tellus,", "id", "interdum", "velit", "laoreet", "id", "donec", "ultrices", "tincidunt", "arcu,", "non", "sodales", "neque", "sodales", "ut", "etiam", "sit", "amet", "nisl", "purus,", "in", "mollis", "nunc",
        "sed", "id", "semper", "risus", "in", "hendrerit", "gravida", "rutrum", "quisque", "non", "tellus", "orci,", "ac", "auctor", "augue", "mauris", "augue", "neque,", "gravida", "in", "fermentum", "et,", "sollicitudin", "ac", "orci", "phasellus", "egestas", "tellus", "rutrum", "tellus", "pellentesque", "eu", "tincidunt", "tortor", "aliquam", "nulla", "facilisi", "cras", "fermentum,", "odio", "eu", "feugiat", "pretium,", "nibh", "ipsum", "consequat", "nisl,", "vel", "pretium", "lectus", "quam", "id", "leo", "in", "vitae", "turpis", "massa", "sed", "elementum", "tempus", "egestas", "sed", "sed", "risus", "pretium", "quam", "vulputate", "dignissim", "suspendisse", "in", "est", "ante", "in", "nibh", "mauris,", "cursus", "mattis", "molestie", "a,", "iaculis", "at", "erat",
        "pellentesque", "adipiscing", "commodo", "elit,", "at", "imperdiet", "dui", "accumsan", "sit", "amet", "nulla", "facilisi", "morbi", "tempus", "iaculis", "urna,", "id", "volutpat", "lacus", "laoreet", "non", "curabitur", "gravida", "arcu", "ac", "tortor", "dignissim", "convallis", "aenean", "et", "tortor", "at", "risus", "viverra", "adipiscing", "at", "in", "tellus", "integer", "feugiat", "scelerisque", "varius", "morbi", "enim", "nunc,", "faucibus", "a", "pellentesque", "sit", "amet,", "porttitor", "eget", "dolor", "morbi", "non", "arcu", "risus,", "quis", "varius", "quam", "quisque", "id", "diam", "vel", "quam", "elementum", "pulvinar", "etiam", "non", "quam", "lacus", "suspendisse", "faucibus", "interdum", "posuere", "lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit", "duis", "tristique", "sollicitudin", "nibh", "sit", "amet", "commodo", "nulla", "facilisi",
        "nullam", "vehicula", "ipsum", "a", "arcu", "cursus", "vitae", "congue", "mauris", "rhoncus", "aenean", "vel", "elit", "scelerisque", "mauris", "pellentesque", "pulvinar", "pellentesque", "habitant", "morbi", "tristique", "senectus", "et", "netus", "et", "malesuada", "fames", "ac", "turpis", "egestas", "maecenas", "pharetra", "convallis", "posuere", "morbi", "leo", "urna,", "molestie", "at", "elementum", "eu,", "facilisis", "sed", "odio", "morbi", "quis", "commodo", "odio", "aenean", "sed", "adipiscing", "diam", "donec", "adipiscing", "tristique", "risus", "nec", "feugiat", "in", "fermentum", "posuere", "urna", "nec", "tincidunt", "praesent", "semper", "feugiat", "nibh", "sed", "pulvinar", "proin", "gravida", "hendrerit", "lectus", "a", "molestie"
    ];
        
    var  dataPlugin = 'plugin_' + Name,

            // default options, used for instantion, if not explicitly set
            defaults = {
			url         : '',
            method: 'get',
            ajaxData    : {},
            debug        : {
                log: false,
                latency: 0
            },
            maskText: false,
            skelParentText: false,
            removeIframe: false,
            backgroundImage: true,
            replaceImageWith: '',
            selector: '',
            incache : false,
            onComplete     : function() {
                _logger('default onComplete() event');
            }
		};


    /**
     *  jQuery screen skeleton - scheletrone
     *
     *  @alias scheletrone
     *  @constructor
     *
     *  @author   Vincenzo Bifano
     *
     *  @requires jquery.js
     *
     *  @param   {Object}        [options]                 - a set of options, to override the defaults
     *  @param   {Function}      [options.onComplete]      - the event is triggered after plugin is complete
     *
     *  @example 
     // minimal setup
        var instance = $('#element').square();

     // customized setup
        var instance = $('#skeleton').skeleton({
                url   : "index2.html",
                debug		: {
                    latency: 3000
                },
                incache: false,
                onComplete	: function() { _logger('plugin complete!'); }
           });

     */



    var Scheletrone  = function(element, options) {
        
        IdElement = $(element).attr('id');

        // This is the plugin's constructor
        // It is instantiated for each matched DOM element
        // The huge comment block above is JSDoc syntax, for generated documentation
        // The name of the constructor is used ONLY internally
        // As a general best-practise, constructors should be Capitalized

        // store the element element
        this.element = $(element);

        // override default options
        // create a new object, with all default settings, overridden only by the init options
        this.options = $.extend( {}, defaults, options );
        debugLog = this.options.debug.log;

        //element to skeletrize
        this.element    = element;
	    this.$container = $( element );


        //this.init();
        this.init();



    };
    /////////////////////////////////////
    //         Private methods         //
    /////////////////////////////////////
    /**
     *  Make the skeleton of a passed element 
     *
     *  @param   {Object}  objToSkeletrize  the element
     */
    var _makeitSkeleton = function (objToSkeletrize) {

                objToSkeletrize.addClass("pending_el ");

    }
    /**
     *  Make a text log 
     *
     *  @param   {string}  message text to log
     */
    var _logger = function (message) {
             
             if (debugLog)
             {
               console.log(message);
             }
    }

    var _replaceBackgroundImage = function (replaceImageWith,element)
    {
        _logger("*** _replaceBackgroundImage ***");
        var bgimage_url = $( element ).css('background-image');
        
        // ^ Either "none" or url("...urlhere..")
        bgimage_url = /^url\((['"]?)(.*)\1\)$/.exec(bgimage_url);
        bgimage_url = bgimage_url ? bgimage_url[2] : ""; // If matched, retrieve url, otherwise ""
        
        var bg_url = $( element ).css('background');
      
        // ^ Either "none" or url("...urlhere..")
        bg_url = /^url\((['"]?)(.*)\1\)$/.exec(bg_url);
        bg_url = bg_url ? bg_url[2] : ""; // If matched, retrieve url, otherwise ""
            

        

  

        if ((bgimage_url != '') || (bg_url != '') ) {
          
            $( element ).replaceWith("<div class='pending_el "+replaceImageWith+"' style='width:"+$( element ).width()+"px;height:"+$( element ).height()+"px;'></div>")
        
        }
        _logger("*** End _replaceBackgroundImage ***");
    }

    var _getAllStyles = function (elem) {
        if (!elem) return []; // Element does not exist, empty list.
        var win = document.defaultView || window, style, styleNode = [];
        if (win.getComputedStyle) { /* Modern browsers */
            
            style = win.getComputedStyle(elem, '');
            for (var i=0; i<style.length; i++) {
                styleNode.push( style[i] + ':' + style.getPropertyValue(style[i]) );
                //               ^name ^           ^ value ^
            }
        } else if (elem.currentStyle) { /* IE */
            style = elem.currentStyle;
            for (var name in style) {
                styleNode.push( name + ':' + style[name] );
            }
        } else { /* Ancient browser..*/
            style = elem.style;
            for (var i=0; i<style.length; i++) {
                styleNode.push( style[i] + ':' + style[style[i]] );
            }
        }
        return styleNode;
    }



    /**
     *  Delete node without data attribute
     *
     *  @param   {Object}  objToSkeletrize  the element
     *  @return  {Object}
     */

    var _retrieveOnlyToCache = function(data)
    {
        _logger("_retrieveOnlyToCache");
        _logger(data);
        var div = document.createElement('div');
        div.innerHTML = data;
        $( div ).children().each(function( index ) {
             _logger('a');
             _logger($(this).data("scheletrone") );
            if ( $(this).data("scheletrone") ) 
            {

            }
            else
            {
                 $( this ).remove();
                //IE11 compatibility issue #2
                //A small Element.remove() polyfill for IE 
                //https://stackoverflow.com/questions/20428877/javascript-remove-doesnt-work-in-ie
                //
                if (!('remove' in Element.prototype)) {
                    Element.prototype['remove'] = function () {
                    if (this.parentNode) {
                        this.parentNode.removeChild(this);
                    }
                    };
                }
            }
         });
        
         _logger("*** Cache Data ***");
         _logger(div.innerHTML);
         return div.innerHTML;
    }

    /**
     *  For an integer randomly
     *
     *  @param   {integer}  min  minimum
     *  @param   {integer}  max  maximum
     *  @return  {integer}
     */
    var _randomInt = function (min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    /**
     *  Count number of words in a text
     *
     *  @param   {string}  s  Text
     *  @return  {integer}
     */

    var _countWords =  function(s){
        s = s.replace(/(^\s*)|(\s*$)/gi,"");//exclude  start and end white-space
        s = s.replace(/[ ]{2,}/gi," ");//2 or more space to 1
        s = s.replace(/\n /,"\n"); // exclude newline with a start spacing
        return s.split(' ').length; 
    }


    /**
     *  Create text with Lore Ipsum words
     *
     *  @param   {integer}  count  number of words
     *  @param   {integer}  lenght  maximum lenght of the sentence
     *  @return  {string}
     */
    //text creator method with parameters: how many, what
    var _createText = function(count, length) {
        
          var wordIndex = _randomInt(0, Words.length - count - 1);
          var newWord = Words.slice(wordIndex, wordIndex + count).join(' ').replace(/[\.\,]/g,'');

         while (length - newWord.length > 0){
            newWord = _addWord(newWord  );
        }
        return newWord;
    
          
        
    }

    var _addWord = function(string) {
          
          var wordIndex = _randomInt(0, Words.length - 1);
          return string + " " +  Words[wordIndex];
    }



    ////////////////////////////////////
    //         Public methods         //
    ////////////////////////////////////
    Scheletrone.prototype = {

        /**
         *  Initializes the scheletrone.
         *  This is automatically called when the plugin is called.
         *
         *  @private
         */
        init: function () {
            var _this  = this.element;
            var __this = this;


            _logger(this);
            // iterate all children in element to make a skeleton
            
            if(this.options.removeIframe)
                jQuery('html').find('iframe').remove();


            if (this.options.incache)
            {
                _logger(this.getCache());
                 
                    this.element.innerHTML = this.getCache();
                   
            }

            

            $( _this ).find('*').each(function( index ) {
              
               

                $( this )
                .contents()
                    .filter(function() {
                        
                        return this.nodeType === 3;
                    })
                    .each(function(  ) {
                        
                        if(this.nodeValue.trim() != '')
                        {
                            _logger(this,"-- " + this.nodeValue.trim() + '--');

                            if (__this.options.maskText)
                            {
                                var numberOfWords = _countWords(this.nodeValue.trim());
                                var newText = _createText(numberOfWords,this.nodeValue.trim().length);
                                
                                this.nodeValue = newText;
                            }
                            if (__this.options.skelParentText)
                            {
                               var color = $( this ).parent().css( {"background-color" : "#ccc"} );
                             _logger(this,color);
                            }
                            return this
                        }
                        else
                        {
                            this.remove();
                              //IE11 compatibility issue #2
                            //A small Element.remove() polyfill for IE 
                            //https://stackoverflow.com/questions/20428877/javascript-remove-doesnt-work-in-ie
                            //
                            if (!('remove' in Element.prototype)) {
                                Element.prototype['remove'] = function () {
                                if (this.parentNode) {
                                    this.parentNode.removeChild(this);
                                }
                                };
                            }
                        }
                            
                    })
                    .wrap( "<div class='nodeType3' ></div>" )
                    .end()
                   
            });

             $( _this ).find('*').each(function( index ) {
                    var skeletizza = true;
                    //search for children
 
                    if (!__this.options.backgroundImage)
                         _replaceBackgroundImage(__this.options.replaceImageWith,this);

                    $( this ).css('color', '#ccc');

                    
                    
                    if($( this ).children().length == 0)
                    {
                                
                                if($( this ).is("BR"))
                                {
                                    skeletizza = false;
                                }

                                if($( this ).is("IMG"))
                                {
                                   
                                    var width = this.width;
                                    var height = this.height;
                                    var tempThis = this;
                                    var replaced = "<div class='pending_el " + __this.options.replaceImageWith + " ' style='width:"+width+"px;height:"+height+"px;)'></div>"
                                    $( this ).replaceWith(replaced);
                          
                                   
                                 
                                    skeletizza = false;
                                }

                                if (skeletizza)
                                {
                                    
                                    _makeitSkeleton($( this ));
                                
                                }
                    }
             });

            
            
     



            if (this.options.url != '')
            {
                _logger('prova');
                this.retrieveData();
            }
            // trigger onComplete callback
            if (this.options.onComplete && typeof(this.options.onComplete) == "function")
                this.options.onComplete();
        },
        retrieveData: function () {
        var obj = this;
 
       
                if (this.options.debug.latency > 0)
                {
                    
                setTimeout(function(){
                 
                            $.ajax({
                                url: obj.options.url,
                                dataType: "html",
                                type: obj.options.method,
                                data: obj.options.ajaxData,
                                success: function(data) {
                                    
                                    _logger(obj.options.debug.log,"obj.element " + obj.element);
                                   
                                      
                                        if (obj.options.selector != '')
                                        {
                                            var parsedResponse = $.parseHTML(data);
                                      
                                            var result = $(parsedResponse).filter(obj.options.selector);
                                            _logger("*** Selector *** ");
                                            _logger(obj.options.selector);
                                            _logger(result.html());
                                            _logger("*** End Selector *** ");
                                            $( obj.element ).html('').append((result));
                                        }
                                        else
                                        {
                                            $( obj.element ).html('').append((data));
                                        }



                                        if (obj.options.incache)
                                        {
                                            _logger(obj.options.debug.log,'setcache');
                                            var cacheData = _retrieveOnlyToCache(data);
                                            obj.setCache(cacheData);
                                        }
                                }
                            });
                    }, obj.options.debug.latency);
                }
                else{
                    
                    $.ajax({
                                url: obj.options.url,
                                dataType: "html",
                                type: obj.options.method,
                                data: obj.options.ajaxData,
                                success: function(data) {
                                    
                                    _logger(obj.options.debug.log,obj);
                                  
                                    if (obj.options.selector != '')
                                    {
                                        //Populate with only a specific content Issue #4
                                        var parsedResponse = $.parseHTML(data);
                                        var result = $(parsedResponse).filter(obj.options.selector);
                                        _logger("*** Selector *** ");
                                        _logger(obj.options.selector);
                                        _logger(result.html());
                                        _logger("*** End Selector *** ");
                                        $( obj.element ).html('').append((result));
                                    }
                                    else
                                    {
                                        $( obj.element ).html('').append((data));
                                    }


                                }
                            });
                }

        },
        /**
         *  Stop loading on div - pass it on construction
         *
         * @example this.stopLoader();
         */
        stopLoader: function () {
            var obj = this;
            $(obj.element).html('');
            
        },
        /**
         *  Store the asynchronus data in localstorage
         *
         *  @example this.setCache(data);
         */
        setCache : function ( result_data ) {
            // Cache data
           
            if ( window.localStorage ) {
                var url = window.location.pathname;
                var filename = url.substring(url.lastIndexOf('/')+1);


                window.localStorage.setItem( filename + "-" + "div-"+IdElement+"-skeleton:" ,  result_data  );
            }
        },
        /**
         *  Retrieve stored scheletrone in localstorage
         *
         *  @example this.getCache();
         */
        getCache : function() {

            if ( window.localStorage ) {
                var url = window.location.pathname;
                var filename = url.substring(url.lastIndexOf('/')+1);
                return window.localStorage.getItem( filename + "-" + "div-"+IdElement+"-skeleton:" );
            }
            else {
                return false;
            }
        },
        
    };



  
    







   //////////////////////////////////////////////////
    //         Plugin wrapper                       //
    //////////////////////////////////////////////////


    // A plugin wrapper around the constructor, preventing against multiple instantiations
    $.fn[Name] = function ( options ) {
        var instance;

        // If the first parameter is an object (options), or was omitted,
        // call Plugin.init()
        if ( typeof options === 'undefined' || typeof options === 'object' ) {
            return this.each(function () {
                // prevent multiple instantiations
                if ( !$.data(this, dataPlugin )) {
                    $.data(
                        this, 
                        dataPlugin, 
                        new Scheletrone( this, options )
                    );
                }

                instance = $(this).data( dataPlugin );

                if ( typeof instance['init'] === 'function' ) {
                    instance.init();
                }
            });

        // checks that the requested public method exists
        } else if ( typeof options === 'string' ) {
            var methodName = arguments[0],
                args = Array.prototype.slice.call(arguments, 1),
                returnVal;

            this.each(function() {
                var instance = $(this).data( dataPlugin );

                // Check that the element has a plugin instance, and that
                // the requested public method exists.
                if ( $.data(this, dataPlugin) && typeof $.data(this, dataPlugin)[methodName] === 'function' ) {
                    // Call the method of the Plugin instance, and Pass it
                    // the supplied arguments.
                    returnVal = $.data(this, dataPlugin)[methodName].apply(instance, args);
                } else {
                    console.info('Method ' + options + ' does not exist on jQuery.' + Name);
                }
            });

            if ( typeof returnVal !== 'undefined' ){
                // If the method returned a value, return the value
                return returnVal;
            } else {
                // Otherwise, returning 'this' preserves chainability
                return this;
            }
        } else {
            console.info('Method ' + options + ' does not exist on jQuery.' + Name);
        }
    };
})( jQuery, window, document );
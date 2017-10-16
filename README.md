# Bookmark-Server
A *bookmark server* or URI shortener that maintains a mapping (dictionary)
between short names and long URIs, checking that each new URI added to the
 mapping actually works .

 This server serves three kinds of requests:
  * A GET request to the / (root) path.  
    >The server returns a form allowing
    the user to submit a new name/URI pairing.  The form also includes a
   listing of all the known pairings.

  * A POST request containing "longuri" and "shortname" fields.  
    >The server
   checks that the URI is valid (by requesting it), and if so, stores the
  mapping from shortname to longuri in its dictionary.  The server then
   redirects back to the root path.
  * A GET request whose path contains a short name.   
    >The server looks up
    that short name in its dictionary and redirects to the corresponding
    long URI.  ex: (/short_name)

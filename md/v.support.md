
## DESCRIPTION

*v.support* is used to set/update vector map metadata. While GRASS
GIS typically generates these metadata entries automatically, *v.support*
allows users to manually edit them when necessary.

## EXAMPLE

```



# update scale to 1:24000
v.support myvectmap scale=24000


# update organization
v.support myvectmap organization="OSGeo labs"
v.info myvectmap


```

## SEE ALSO

*[v.build](v.build.html),
[v.info](v.info.html)*

## AUTHOR

Markus Neteler, Trento

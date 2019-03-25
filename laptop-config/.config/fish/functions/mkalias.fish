function mkalias --argument key value
  echo alias $key=$value
  alias $key=$value
  funcsave $key
end

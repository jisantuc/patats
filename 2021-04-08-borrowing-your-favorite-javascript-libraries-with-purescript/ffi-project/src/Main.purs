module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)
import SimpleFFI (leftPad)

main :: Effect Unit
main = do
  log $ leftPad "abcde" 10 "b"
  log $ leftPad "batman" 32 "na"

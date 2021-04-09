module SimpleFFI where

import Prelude

import Data.Function.Uncurried (Fn3, runFn3)

-- foreign import padLeft :: Fn3 String Int String String
-- foreign import leftPadImpl :: Fn3 String Int String String

-- leftPad :: String -> Int -> String -> String
-- leftPad s n l = runFn3 leftPadImpl s n l
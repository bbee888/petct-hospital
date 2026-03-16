import { defineConfig, presetUno, presetAttributify, presetIcons } from 'unocss'
import epIcons from '@iconify-json/ep'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      prefix: 'i-ep-',
      collections: {
        ep: epIcons.icons
      },
      extraProperties: {
        'display': 'inline-block',
        'vertical-align': 'middle'
      }
    })
  ]
})

import { defineConfig } from 'unocss'
import presetIcons from '@unocss/preset-icons'
import epIcons from '@iconify-json/ep'

export default defineConfig({
  presets: [
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

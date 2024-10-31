export const appOptions = [
  { value: 'Temperature regulation effect conflict', label: 'Temperature regulation effect conflict' },
  { value: 'Brightness regulation', label: 'Brightness regulation' },
  { value: 'Raining/Window conflict', label: 'Raining/Window conflict' },
  { value: 'Unsafe use of microwave oven', label: 'Unsafe use of microwave oven' },
  { value: 'Unsafe use of water dispenser', label: 'Unsafe use of water dispenser' },
  { value: 'Excessive humidity', label: 'Excessive humidity' },
  { value: 'Low air quality', label: 'Low air quality' },
  { value: 'Waste of electricity', label: 'Waste of electricity' },
  { value: 'Drinking fountains work too long', label: 'Drinking fountains work too long' },
  { value: 'Excessive noise', label: 'Excessive noise' }
]

export const categoryOptions = [
  { value: 'Spatial State', label: 'Spatial State', description: '' },
  { value: 'Temporal Trace', label: 'Temporal Trace', description: '' }
]

export const radioOptions = [
  { value: 'Always', label: 'Always' },
  { value: 'Never', label: 'Never' }
]

export const tempTemplateOptions = {
  'Temporal Trace': [
    { value: 'event-state-time', label: 'event-state-time', description: 'The [State] [always/never] occur within the [Time] of the [Event] occurrence.' },
    { value: 'effect-time', label: 'effect-time', description: 'The execution time of the [Effect] must be [greater than/less than] [Time].' },
    { value: 'state-time', label: 'state-time', description: 'The duration of the [State] must be [greater than/less than] [Time].' },
    { value: 'effect-state-time', label: 'effect-state-time', description: 'The [Effect] [always/never] happen within the [Time] while [state1, ..., staten].' }
  ],
  'Spatial State': [
    { value: 'effect-effect', label: 'effect-effect', description: 'Multiple [effect] [always/never] occur at the same time.' },
    { value: 'state-state', label: 'state-state', description: '[state1, ..., staten] should [always/never] be active at the same time.' },
    { value: 'event-state', label: 'event-state', description: '[Event] should [always/never] happen while [state1, ..., staten].' },
    { value: 'effect-state', label: 'effect-state', description: '[effect] should [always/never] happen while [state1, ..., staten].' }
  ]
}

export const symbolOptions = [
  { value: '>', label: '>' },
  { value: '<', label: '<' }
]

export const typeOptions = [
  { value: 'event', label: 'event' },
  { value: 'action', label: 'action' }
]

export const enviromentOptions = [
  { value: 'Lab', label: 'Lab' },
  { value: 'Home', label: 'Home' }
]

export const resolveOptions = [
  { value: 'Revoke', label: 'Revoke' },
  { value: 'Substitute', label: 'Substitute' },
  { value: 'Notify', label: 'Notify' },
  { value: 'Environment Adjust', label: 'Environment Adjust' }
]

import axios from 'axios'

export default {
  getPreConditionLTL (preCondition) {
    let ltl = ''
    if (preCondition !== '') {
      const preConditionList = preCondition.split(' ')
      if (preConditionList.length === 3) {
        let tempOneList = ''
        let tempTwoList = ''
        if (preConditionList[1] === '>') {
          tempOneList = preConditionList[0]
          tempTwoList = preConditionList[2]
        } else if (preConditionList[1] === '<') {
          tempOneList = preConditionList[2]
          tempTwoList = preConditionList[0]
        }
        ltl = '(' + tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'middle' + ')|(' + tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'low' + ')|(' + tempOneList + '.' + 'middle' + ' & ' + tempTwoList + '.' + 'low' + ')'
      } else if (preConditionList.length === 5) {
        const tempOneList = preConditionList[0]
        const tempTwoList = preConditionList[2]
        if (preConditionList[4] === '2') {
          ltl = tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'low'
        } else if (preConditionList[4] === '-2') {
          ltl = tempOneList + '.' + 'low' + ' & ' + tempTwoList + '.' + 'high'
        }
      } else if (preConditionList.length === 7 && (preConditionList.indexOf('&&') !== -1)) {
        let tempOneList = ''
        let tempTwoList = ''
        if (preConditionList[1] === '>') {
          tempOneList = preConditionList[0]
          tempTwoList = preConditionList[2]
        } else if (preConditionList[1] === '<') {
          tempOneList = preConditionList[2]
          tempTwoList = preConditionList[0]
        }
        ltl = '((' + tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'middle' + ')|(' + tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'low' + ')|(' + tempOneList + '.' + 'middle' + ' & ' + tempTwoList + '.' + 'low' + '))'
        if (preConditionList[6] === '0') {
          ltl = ltl + ' & ' + preConditionList[4] + '.' + 'off'
        } else if (preConditionList[6] === '1') {
          ltl = ltl + ' & ' + preConditionList[4] + '.' + 'on'
        }
      } else if (preConditionList.length === 11 && (preConditionList.indexOf('&&') !== -1)) {
        let tempOneList = ''
        let tempTwoList = ''
        if (preConditionList[1] === '>') {
          tempOneList = preConditionList[0]
          tempTwoList = preConditionList[2]
        } else if (preConditionList[1] === '<') {
          tempOneList = preConditionList[2]
          tempTwoList = preConditionList[0]
        }
        ltl = '((' + tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'middle' + ')|(' + tempOneList + '.' + 'high' + ' & ' + tempTwoList + '.' + 'low' + ')|(' + tempOneList + '.' + 'middle' + ' & ' + tempTwoList + '.' + 'low' + '))'
        if (preConditionList[6] === '0') {
          ltl = ltl + ' & ' + preConditionList[4] + '.' + 'off'
        } else if (preConditionList[6] === '1') {
          ltl = ltl + ' & ' + preConditionList[4] + '.' + 'on'
        }
        if (preConditionList[10] === '0') {
          ltl = ltl + ' & ' + preConditionList[8] + '.' + 'off'
        } else if (preConditionList[10] === '1') {
          ltl = ltl + ' & ' + preConditionList[8] + '.' + 'on'
        }
      }
    }
    return ltl
  },
  async getLTL (list) {
    let ltl = ''
    const that = this
    for (let i = 0; i < list.length; i++) {
      await axios.get('/api/effect_node/' + list[i].location + '/effect_' + list[i].effect, {
        headers: {
          'Content-Type': 'application/text'
        }
      }).then(res => {
        const results = res.data
        let ltlEffect = ''
        for (let j = 0; j < results.length; j++) {
          let ltlAction = ''
          const result = results[j]
          const actionItem = result.room + '.' + result.device.substring(0, result.device.length - 3) + '.' + result.action.substring(7, result.action.length)
          ltlAction = actionItem
          const preConditionItem = that.getPreConditionLTL(result.pre_condition)
          if (preConditionItem !== '') {
            ltlAction = ltlAction + ' & ' + '(' + preConditionItem + ')'
          }
          if (ltlAction !== '') {
            ltlEffect = ltlEffect + ' | ' + '(' + ltlAction + ')'
          }
        }
        ltlEffect = ltlEffect.substring(3, ltlEffect.length)
        if (ltlEffect !== '') {
          ltl = ltl + ' & ' + '(' + ltlEffect + ')'
        }
      }).catch(err => {
        console.log(err)
      })
    }
    return ltl
  }
}
